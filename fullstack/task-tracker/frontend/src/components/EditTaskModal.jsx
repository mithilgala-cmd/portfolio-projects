import { AlertTriangle, X } from 'lucide-react'
import { useEffect, useRef, useState } from 'react'

const PRIORITY_OPTIONS = [
  { value: 'low', label: 'Low' },
  { value: 'medium', label: 'Medium' },
  { value: 'high', label: 'High' },
]

function EditTaskModal({ task, onSave, onClose, isSaving }) {
  const [title, setTitle] = useState(task.title)
  const [description, setDescription] = useState(task.description)
  const [priority, setPriority] = useState(task.priority)
  const [error, setError] = useState('')
  const titleRef = useRef(null)

  // Focus title on open
  useEffect(() => {
    titleRef.current?.focus()
  }, [])

  // Close on Escape
  useEffect(() => {
    function onKey(e) {
      if (e.key === 'Escape') onClose()
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [onClose])

  async function handleSubmit(e) {
    e.preventDefault()
    const trimmedTitle = title.trim()
    if (!trimmedTitle) {
      setError('Title cannot be empty.')
      return
    }
    setError('')
    await onSave(task.id, {
      title: trimmedTitle,
      description: description.trim(),
      priority,
    })
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-card" onClick={(e) => e.stopPropagation()} role="dialog" aria-modal="true" aria-labelledby="edit-modal-title">
        <div className="modal-header">
          <h2 id="edit-modal-title">Edit Task</h2>
          <button type="button" className="modal-close-btn" onClick={onClose} aria-label="Close modal">
            <X size={18} />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="modal-form">
          <div className="modal-field">
            <label htmlFor="edit-title">Title</label>
            <input
              ref={titleRef}
              id="edit-title"
              type="text"
              value={title}
              maxLength={120}
              onChange={(e) => setTitle(e.target.value)}
              disabled={isSaving}
              required
            />
          </div>

          <div className="modal-field">
            <label htmlFor="edit-description">Description</label>
            <textarea
              id="edit-description"
              value={description}
              maxLength={500}
              rows={3}
              onChange={(e) => setDescription(e.target.value)}
              disabled={isSaving}
            />
          </div>

          <div className="modal-field">
            <label>Priority</label>
            <div className="priority-selector">
              {PRIORITY_OPTIONS.map((opt) => (
                <button
                  key={opt.value}
                  type="button"
                  className={`priority-option priority-option--${opt.value}${priority === opt.value ? ' selected' : ''}`}
                  onClick={() => setPriority(opt.value)}
                  disabled={isSaving}
                >
                  {opt.label}
                </button>
              ))}
            </div>
          </div>

          {error && (
            <p className="modal-error">
              <AlertTriangle size={14} /> {error}
            </p>
          )}

          <div className="modal-actions">
            <button type="button" className="secondary-btn" onClick={onClose} disabled={isSaving}>
              Cancel
            </button>
            <button type="submit" className="primary-btn" disabled={isSaving}>
              {isSaving ? 'Saving...' : 'Save Changes'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default EditTaskModal
