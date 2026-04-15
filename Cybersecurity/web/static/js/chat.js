/**
 * Secure Chat Frontend - JavaScript
 * Handles real-time messaging, encryption visualization, and UI updates
 */

let currentUser = null;
let selectedPeer = null;
let messageCount = { sent: 0, received: 0 };
let peerKeysCached = 0;

// Message polling interval
let messagePoller = null;

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initializeChat();
    loadSecurityInfo();
    startMessagePolling();
});

/**
 * Initialize chat interface
 */
function initializeChat() {
    const usernameElement = document.querySelector('.username');
    if (usernameElement) {
        currentUser = usernameElement.textContent.replace('👤 ', '').trim();
    }
    
    // Add click handlers to user items
    document.querySelectorAll('.user-item').forEach(item => {
        item.addEventListener('click', function() {
            selectUser(this.textContent.toLowerCase().trim());
        });
    });
    
    // Message form handler
    const messageForm = document.getElementById('message-form');
    if (messageForm) {
        messageForm.addEventListener('submit', sendMessage);
    }
}

/**
 * Load and display security information
 */
function loadSecurityInfo() {
    fetch('/api/security_info')
        .then(response => response.json())
        .then(data => {
            updateSecurityPanel(data);
        })
        .catch(error => console.error('Error loading security info:', error));
}

/**
 * Update security panel with info from backend
 */
function updateSecurityPanel(data) {
    const panel = document.getElementById('security-panel');
    if (!panel) return;
    
    let html = '';
    const technical = data.technical_details;
    
    html += `
        <div class="security-item">
            <strong>User Auth:</strong>
            <code>PBKDF2 (${technical.hash_iterations}k)</code>
        </div>
        <div class="security-item">
            <strong>Message:</strong>
            <code>AES-256</code>
        </div>
        <div class="security-item">
            <strong>Key Exchange:</strong>
            <code>RSA-${technical.rsa_key_size}b</code>
        </div>
        <div class="security-item">
            <strong>Salt Size:</strong>
            <code>${technical.salt_size * 8} bits</code>
        </div>
    `;
    
    panel.innerHTML = html;
}

/**
 * Select a user to chat with
 */
function selectUser(username) {
    selectedPeer = username;
    
    // Update UI
    document.querySelectorAll('.user-item').forEach(item => {
        item.classList.remove('active');
    });
    
    event.target.closest('.user-item').classList.add('active');
    
    // Update chat header
    document.getElementById('chat-title').textContent = `💬 Chat with ${username}`;
    
    // Clear messages
    const container = document.getElementById('messages-container');
    container.innerHTML = '';
    
    // Add welcome message
    const welcome = document.createElement('div');
    welcome.className = 'welcome-message';
    welcome.innerHTML = `
        <h3>Starting chat with ${username}</h3>
        <p>All messages are encrypted end-to-end.</p>
        <p style="font-size: 12px; color: var(--text-tertiary); margin-top: 12px;">
            🔐 Each message uses a unique AES-256-CBC key wrapped with ${username}'s RSA-2048 public key
        </p>
    `;
    container.appendChild(welcome);
    
    // Enable message input
    const input = document.getElementById('message-input');
    const sendBtn = document.getElementById('send-btn');
    input.disabled = false;
    sendBtn.disabled = false;
    input.placeholder = `Message to ${username}...`;
    input.focus();
}

/**
 * Send encrypted message
 */
async function sendMessage(event) {
    event.preventDefault();
    
    if (!selectedPeer) {
        showNotification('Please select a user first', 'error');
        return;
    }
    
    const messageInput = document.getElementById('message-input');
    const message = messageInput.value.trim();
    
    if (!message) {
        return;
    }
    
    // Show sending state
    const sendBtn = document.getElementById('send-btn');
    const originalText = sendBtn.textContent;
    sendBtn.textContent = '⏳ Sending...';
    sendBtn.disabled = true;
    
    try {
        const response = await fetch('/api/send_message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                peer: selectedPeer,
                message: message
            })
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            // Add message to UI
            displayMessage(currentUser, message, true);
            messageCount.sent++;
            updateStats();
            
            // Clear input
            messageInput.value = '';
        } else {
            showNotification(data.error || 'Failed to send message', 'error');
        }
    } catch (error) {
        console.error('Error sending message:', error);
        showNotification('Error sending message', 'error');
    } finally {
        sendBtn.textContent = originalText;
        sendBtn.disabled = false;
        messageInput.focus();
    }
}

/**
 * Display message in chat
 */
function displayMessage(sender, messageText, sent = false) {
    const container = document.getElementById('messages-container');
    
    // Remove welcome message if first message
    const welcome = container.querySelector('.welcome-message');
    if (welcome && (container.children.length === 1 || 
        (container.children.length === 2 && container.children[1].classList.contains('message')))) {
        // Keep welcome
    } else if (welcome) {
        welcome.remove();
    }
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sent ? 'sent' : 'received'}`;
    
    const now = new Date();
    const timeStr = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    
    messageDiv.innerHTML = `
        <div class="message-content">
            <div class="message-text">${escapeHtml(messageText)}</div>
            <div class="message-meta">
                <span>${timeStr}</span>
                <span class="encryption-badge">🔐 E2EE</span>
            </div>
        </div>
    `;
    
    container.appendChild(messageDiv);
    container.scrollTop = container.scrollHeight;
}

/**
 * Poll for new messages from server
 */
function startMessagePolling() {
    messagePoller = setInterval(pollMessages, 2000);
}

/**
 * Poll for incoming messages
 */
async function pollMessages() {
    try {
        const response = await fetch('/api/get_messages');
        const data = await response.json();
        
        if (data.messages && data.messages.length > 0) {
            data.messages.forEach(msg => {
                if (msg.type === 'error') {
                    showNotification(msg.message, 'error');
                } else {
                    displayMessage(msg.from, msg.message, false);
                    messageCount.received++;
                    updateStats();
                }
            });
        }
    } catch (error) {
        console.error('Error polling messages:', error);
    }
}

/**
 * Update statistics display
 */
function updateStats() {
    document.getElementById('sent-count').textContent = messageCount.sent;
    document.getElementById('recv-count').textContent = messageCount.received;
}

/**
 * Show notification/toast
 */
function showNotification(message, type = 'info') {
    // Could implement a toast notification here
    console.log(`[${type.toUpperCase()}] ${message}`);
    
    if (type === 'error') {
        alert(message);
    }
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Visual encryption flow animation (for demo)
 */
function animateEncryption() {
    const flows = document.querySelectorAll('.encryption-flow');
    flows.forEach(flow => {
        flow.style.animation = 'slideIn 0.6s ease-out';
    });
}

/**
 * Update connection status
 */
function updateConnectionStatus(connected = true) {
    const statusIndicator = document.getElementById('status-indicator');
    if (statusIndicator) {
        if (connected) {
            statusIndicator.textContent = '● Connected';
            statusIndicator.classList.add('connected');
        } else {
            statusIndicator.textContent = '● Disconnected';
            statusIndicator.classList.remove('connected');
        }
    }
}

// Cleanup on page unload
window.addEventListener('unload', () => {
    if (messagePoller) {
        clearInterval(messagePoller);
    }
});
