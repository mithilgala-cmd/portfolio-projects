import { AlertTriangle, CheckCircle2, ListTodo, Timer } from 'lucide-react'
import { useCallback, useEffect, useMemo, useState } from 'react'
import TaskColumn from './components/TaskColumn'
import TaskComposer from './components/TaskComposer'
import { createTask, deleteTask, fetchTasks, updateTaskStatus } from './services/tasks'

const STATUS_GROUPS = [
  { key: 'todo', title: 'Planned', accent: '#ff8f6f' },
  { key: 'in_progress', title: 'In Motion', accent: '#f5b85d' },
  { key: 'done', title: 'Delivered', accent: '#56bf8c' },
]

function App() {
  const [tasks, setTasks] = useState([])
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  const loadTasks = useCallback(async () => {
    setLoading(true)
    setError('')
    try {
      const data = await fetchTasks()
      setTasks(data)
    } catch {
      setError('Unable to reach the Task Tracker API. Make sure backend is running.')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    void loadTasks()
  }, [loadTasks])

  async function handleCreate(payload) {
    setSubmitting(true)
    setError('')
    setSuccess('')
    try {
      const created = await createTask(payload)
      setTasks((current) => [...current, created])
      setSuccess('Task added successfully.')
    } catch {
      setError('Could not create task. Please try again.')
    } finally {
      setSubmitting(false)
    }
  }

  async function handleStatusChange(taskId, status) {
    setError('')
    setSuccess('')
    try {
      const updated = await updateTaskStatus(taskId, status)
      setTasks((current) => current.map((task) => (task.id === taskId ? updated : task)))
      setSuccess('Task status updated.')
    } catch {
      setError('Status update failed. Refresh and try again.')
    }
  }

  async function handleDelete(taskId) {
    setError('')
    setSuccess('')
    try {
      await deleteTask(taskId)
      setTasks((current) => current.filter((task) => task.id !== taskId))
      setSuccess('Task deleted.')
    } catch {
      setError('Delete failed. Please retry.')
    }
  }

  const stats = useMemo(() => {
    const total = tasks.length
    const done = tasks.filter((task) => task.status === 'done').length
    const inProgress = tasks.filter((task) => task.status === 'in_progress').length
    const completion = total === 0 ? 0 : Math.round((done / total) * 100)
    return { total, done, inProgress, completion }
  }, [tasks])

  return (
    <div className="app-shell">
      <div className="background-layer" />
      <main className="app-content">
        <header className="hero">
          <div className="hero-copy">
            <p className="eyebrow">Task Tracker Pro</p>
            <h1>Free tooling, premium execution.</h1>
            <p>
              This React client is designed to work with your FastAPI + Supabase backend and gives a
              modern workspace for planning, execution, and delivery.
            </p>
          </div>
          <div className="stats-grid">
            <article>
              <span>
                <ListTodo size={16} /> Total Tasks
              </span>
              <strong>{stats.total}</strong>
            </article>
            <article>
              <span>
                <Timer size={16} /> In Motion
              </span>
              <strong>{stats.inProgress}</strong>
            </article>
            <article>
              <span>
                <CheckCircle2 size={16} /> Completion
              </span>
              <strong>{stats.completion}%</strong>
            </article>
          </div>
        </header>

        <section className="workspace">
          <TaskComposer onCreate={handleCreate} isSubmitting={submitting} />

          {error && (
            <div className="banner error">
              <AlertTriangle size={16} />
              {error}
            </div>
          )}

          {success && <div className="banner success">{success}</div>}

          {loading ? (
            <div className="loading">Loading tasks...</div>
          ) : (
            <div className="board">
              {STATUS_GROUPS.map((group) => (
                <TaskColumn
                  key={group.key}
                  title={group.title}
                  accent={group.accent}
                  tasks={tasks.filter((task) => task.status === group.key)}
                  onStatusChange={handleStatusChange}
                  onDelete={handleDelete}
                />
              ))}
            </div>
          )}
        </section>
      </main>
    </div>
  )
}

export default App
