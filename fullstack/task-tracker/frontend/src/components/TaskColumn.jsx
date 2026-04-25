import { CheckCircle2, Circle, LoaderCircle, Trash2 } from 'lucide-react'

const STATUS_OPTIONS = [
  { value: 'todo', label: 'To Do' },
  { value: 'in_progress', label: 'In Progress' },
  { value: 'done', label: 'Done' },
]

function TaskColumn({ title, tasks, accent, onStatusChange, onDelete }) {
  return (
    <section className="task-column" style={{ '--column-accent': accent }}>
      <header className="task-column-header">
        <h3>{title}</h3>
        <span>{tasks.length}</span>
      </header>

      {tasks.length === 0 && <p className="column-empty">No tasks here yet.</p>}

      <div className="task-list">
        {tasks.map((task, index) => (
          <article className="task-card" key={task.id} style={{ animationDelay: `${index * 60}ms` }}>
            <h4>{task.title}</h4>
            {task.description && <p>{task.description}</p>}

            <div className="task-actions">
              <div className="status-buttons">
                {STATUS_OPTIONS.map((option) => (
                  <button
                    key={`${task.id}-${option.value}`}
                    type="button"
                    className={task.status === option.value ? 'status-btn active' : 'status-btn'}
                    onClick={() => onStatusChange(task.id, option.value)}
                    aria-label={`Set ${task.title} to ${option.label}`}
                  >
                    {option.value === 'todo' && <Circle size={14} />}
                    {option.value === 'in_progress' && <LoaderCircle size={14} />}
                    {option.value === 'done' && <CheckCircle2 size={14} />}
                    {option.label}
                  </button>
                ))}
              </div>

              <button
                type="button"
                className="delete-btn"
                onClick={() => onDelete(task.id)}
                aria-label={`Delete ${task.title}`}
              >
                <Trash2 size={16} />
              </button>
            </div>
          </article>
        ))}
      </div>
    </section>
  )
}

export default TaskColumn
