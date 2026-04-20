/**
 * Secure Chat Frontend - JavaScript
 * Handles message flow and UI updates for the Flask web interface.
 */

let currentUser = null;
let selectedPeer = null;
let messageCount = { sent: 0, received: 0 };
let messagePoller = null;

function initializeMessageCount() {
    const stored = localStorage.getItem('messageCount');
    if (stored) {
        try {
            messageCount = JSON.parse(stored);
        } catch {
            messageCount = { sent: 0, received: 0 };
        }
    }
}

function saveMessageCount() {
    localStorage.setItem('messageCount', JSON.stringify(messageCount));
}

document.addEventListener('DOMContentLoaded', () => {
    initializeMessageCount();
    initializeChat();
    loadSecurityInfo();
    startMessagePolling();
    updateStats();
});

function initializeChat() {
    const usernameElement = document.querySelector('.username');
    if (usernameElement) {
        currentUser = usernameElement.textContent.replace(/^[^A-Za-z0-9_]+/, '').trim().toLowerCase();
    }

    document.querySelectorAll('.user-item').forEach((item) => {
        item.addEventListener('click', () => {
            const username = item.dataset.username || item.textContent.toLowerCase().trim();
            selectUser(username, item);
        });
    });

    const messageForm = document.getElementById('message-form');
    if (messageForm) {
        messageForm.addEventListener('submit', sendMessage);
    }
}

function loadSecurityInfo() {
    fetch('/api/security_info')
        .then((response) => response.json())
        .then((data) => updateSecurityPanel(data))
        .catch((error) => console.error('Error loading security info:', error));
}

function updateSecurityPanel(data) {
    const panel = document.getElementById('security-panel');
    if (!panel) return;

    const technical = data.technical_details || {};
    const iterations = Number(technical.hash_iterations || 100000).toLocaleString();
    const rsaKeySize = Number(technical.rsa_key_size || 2048);
    const saltBits = Number(technical.salt_size_bytes || 16) * 8;

    panel.innerHTML = `
        <div class="security-item">
            <strong>User Auth:</strong>
            <code>PBKDF2 (${iterations})</code>
        </div>
        <div class="security-item">
            <strong>Message:</strong>
            <code>AES-256</code>
        </div>
        <div class="security-item">
            <strong>Key Exchange:</strong>
            <code>RSA-${rsaKeySize}</code>
        </div>
        <div class="security-item">
            <strong>Salt Size:</strong>
            <code>${saltBits} bits</code>
        </div>
    `;
}

function selectUser(username, clickedElement = null) {
    selectedPeer = username;

    document.querySelectorAll('.user-item').forEach((item) => {
        item.classList.remove('active');
    });

    if (clickedElement) {
        clickedElement.classList.add('active');
    }

    const chatTitle = document.getElementById('chat-title');
    if (chatTitle) {
        chatTitle.textContent = `Chat with ${username}`;
    }

    const container = document.getElementById('messages-container');
    if (!container) return;

    container.innerHTML = '';

    const welcome = document.createElement('div');
    welcome.className = 'welcome-message';
    welcome.innerHTML = `
        <h3>Starting chat with ${username}</h3>
        <p>All messages are encrypted end-to-end.</p>
        <p style="font-size: 12px; color: var(--text-tertiary); margin-top: 12px;">
            Each message uses a unique AES-256 key wrapped with ${username}'s RSA public key.
        </p>
    `;
    container.appendChild(welcome);

    const input = document.getElementById('message-input');
    const sendBtn = document.getElementById('send-btn');
    if (input && sendBtn) {
        input.disabled = false;
        sendBtn.disabled = false;
        input.placeholder = `Message to ${username}...`;
        input.focus();
    }
}

async function sendMessage(event) {
    event.preventDefault();

    if (!selectedPeer) {
        showNotification('Please select a user first', 'error');
        return;
    }

    const messageInput = document.getElementById('message-input');
    if (!messageInput) return;

    const message = messageInput.value.trim();
    if (!message) return;

    const sendBtn = document.getElementById('send-btn');
    const originalText = sendBtn ? sendBtn.textContent : 'Send';

    if (sendBtn) {
        sendBtn.textContent = 'Sending...';
        sendBtn.disabled = true;
    }

    try {
        const response = await fetch('/api/send_message', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                peer: selectedPeer,
                message,
            }),
        });

        const data = await response.json();

        if (response.ok && data.success) {
            displayMessage(currentUser, message, true);
            messageCount.sent += 1;
            saveMessageCount();
            updateStats();
            messageInput.value = '';
        } else {
            showNotification(data.error || 'Failed to send message', 'error');
        }
    } catch (error) {
        console.error('Error sending message:', error);
        showNotification('Error sending message', 'error');
    } finally {
        if (sendBtn) {
            sendBtn.textContent = originalText;
            sendBtn.disabled = false;
        }
        messageInput.focus();
    }
}

function displayMessage(sender, messageText, sent = false) {
    const container = document.getElementById('messages-container');
    if (!container) return;

    const welcome = container.querySelector('.welcome-message');
    if (welcome && container.children.length > 1) {
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
                <span class="encryption-badge">E2EE</span>
            </div>
        </div>
    `;

    container.appendChild(messageDiv);
    container.scrollTop = container.scrollHeight;
}

function startMessagePolling() {
    messagePoller = setInterval(pollMessages, 2000);
}

async function pollMessages() {
    try {
        const response = await fetch('/api/get_messages');
        const data = await response.json();

        if (data.messages && data.messages.length > 0) {
            data.messages.forEach((msg) => {
                if (msg.type === 'error') {
                    showNotification(msg.message, 'error');
                } else {
                    displayMessage(msg.from, msg.message, false);
                    messageCount.received += 1;
                    saveMessageCount();
                    updateStats();
                }
            });
        }
    } catch (error) {
        console.error('Error polling messages:', error);
    }
}

function updateStats() {
    const sent = document.getElementById('sent-count');
    const recv = document.getElementById('recv-count');
    if (sent) sent.textContent = messageCount.sent;
    if (recv) recv.textContent = messageCount.received;
}

function showNotification(message, type = 'info') {
    console.log(`[${type.toUpperCase()}] ${message}`);
    if (type === 'error') {
        alert(message);
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

window.addEventListener('unload', () => {
    if (messagePoller) {
        clearInterval(messagePoller);
    }
});
