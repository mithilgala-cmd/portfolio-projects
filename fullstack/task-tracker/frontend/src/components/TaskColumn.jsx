import { CheckCircle2, Circle, LoaderCircle, Pencil, Trash2 } from 'lucide-react'

const STATUS_OPTIONS = [
  { value: 'todo', label: 'To Do', Icon: Circle },
  { value: 'in_progress', label: 'In Progress', Icon: LoaderCircle },
  { value: 'done', label: 'Done', Icon: CheckCircle2 },
]

const PRIORITY_META = {
  high:   { label: 'High',   className: 'badge badge--high' },
  medium: { label: 'Medium', className: 'badge badge--medium' },
  low:    { label: 'Low',    className: 'badge badge--low' },
}

function formatDate(iso) {
  return new Date(iso).toLocaleDateString(undefined, {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  })
}

function TaskColumn({ title, tasks, accent, onStatusChange, onDelete, onEdit }) {
  return (
    <section className="task-column" style={{ '--column-accent': accent }}>
      <header className="task-column-header">
        <h3>{title}</h3>
        <span>{tasks.length}</span>
      </header>

      {tasks.length === 0 && <p className="column-empty">No tasks here yet.</p>}

      <div className="task-list">
        {tasks.map((task, index) => {
          const priority = PRIORITY_META[task.priority] ?? PRIORITY_META.medium
          return (
            <article
              className="task-card"
              key={task.id}
              style={{ animationDelay: `${index * 60}ms` }}
            >
              <div className="task-card-top">
                <h4>{task.title}</h4>
                <span className={priority.className}>{priority.label}</span>
              </div>

              {task.description && <p>{task.description}</p>}

              <p className="task-meta">Added {formatDate(task.created_at)}</p>

              <div className="task-actions">
                <div className="status-buttons">
                  {STATUS_OPTIONS.map(({ value, label, Icon }) => (
                    <button
                      key={`${task.id}-${value}`}
                      type="button"
                      className={task.status === value ? 'status-btn active' : 'status-btn'}
                      onClick={() => onStatusChange(task.id, value)}
                      aria-label={`Set ${task.title} to ${label}`}
                    >
                      <Icon size={14} />
                      {label}
                    </button>
                  ))}
                </div>

                <div className="card-icon-actions">
                  <button
                    type="button"
                    className="icon-btn edit-btn"
                    onClick={() => onEdit(task)}
                    aria-label={`Edit ${task.title}`}
                  >
                    <Pencil size={15} />
                  </button>
                  <button
                    type="button"
                    className="icon-btn delete-btn"
                    onClick={() => onDelete(task.id)}
                    aria-label={`Delete ${task.title}`}
                  >
                    <Trash2 size={15} />
                  </button>
                </div>
              </div>
            </article>
          )
        })}
      </div>
    </section>
  )
}

export default TaskColumn
