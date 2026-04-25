import { Plus } from 'lucide-react'
import { useState } from 'react'

const PRIORITY_OPTIONS = [
  { value: 'low', label: 'Low' },
  { value: 'medium', label: 'Medium' },
  { value: 'high', label: 'High' },
]

function TaskComposer({ onCreate, isSubmitting }) {
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [priority, setPriority] = useState('medium')

  async function handleSubmit(event) {
    event.preventDefault()
    const trimmedTitle = title.trim()
    if (!trimmedTitle) return

    await onCreate({
      title: trimmedTitle,
      description: description.trim(),
      priority,
    })
    setTitle('')
    setDescription('')
    setPriority('medium')
  }

  return (
    <form className="composer" onSubmit={handleSubmit}>
      <div className="composer-row">
        <label htmlFor="task-title">Task title</label>
        <input
          id="task-title"
          type="text"
          placeholder="e.g. Ship the landing page"
          maxLength={120}
          value={title}
          onChange={(event) => setTitle(event.target.value)}
          disabled={isSubmitting}
          required
        />
      </div>

      <div className="composer-row">
        <label htmlFor="task-description">Description</label>
        <input
          id="task-description"
          type="text"
          placeholder="Optional notes or context"
          maxLength={500}
          value={description}
          onChange={(event) => setDescription(event.target.value)}
          disabled={isSubmitting}
        />
      </div>

      <div className="composer-row">
        <label htmlFor="task-priority">Priority</label>
        <select
          id="task-priority"
          value={priority}
          onChange={(e) => setPriority(e.target.value)}
          disabled={isSubmitting}
          className="priority-select"
        >
          {PRIORITY_OPTIONS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </div>

      <button type="submit" className="primary-btn" disabled={isSubmitting}>
        <Plus size={18} />
        {isSubmitting ? 'Adding...' : 'Add Task'}
      </button>
    </form>
  )
}

export default TaskComposer
