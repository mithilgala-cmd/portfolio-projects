import { Plus } from 'lucide-react'
import { useState } from 'react'

function TaskComposer({ onCreate, isSubmitting }) {
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')

  async function handleSubmit(event) {
    event.preventDefault()
    const trimmedTitle = title.trim()
    if (!trimmedTitle) {
      return
    }

    await onCreate({
      title: trimmedTitle,
      description: description.trim(),
    })
    setTitle('')
    setDescription('')
  }

  return (
    <form className="composer" onSubmit={handleSubmit}>
      <div className="composer-row">
        <label htmlFor="task-title">Task title</label>
        <input
          id="task-title"
          type="text"
          placeholder="Ship a premium free experience"
          maxLength={120}
          value={title}
          onChange={(event) => setTitle(event.target.value)}
          disabled={isSubmitting}
          required
        />
      </div>

      <div className="composer-row">
        <label htmlFor="task-description">Description</label>
        <textarea
          id="task-description"
          placeholder="Write details, notes, links, or acceptance criteria."
          maxLength={500}
          rows={4}
          value={description}
          onChange={(event) => setDescription(event.target.value)}
          disabled={isSubmitting}
        />
      </div>

      <button type="submit" className="primary-btn" disabled={isSubmitting}>
        <Plus size={18} />
        {isSubmitting ? 'Adding...' : 'Add Task'}
      </button>
    </form>
  )
}

export default TaskComposer
