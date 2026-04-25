import { AlertTriangle, CheckCircle2, ListTodo, Search, Timer, X } from 'lucide-react'
import { useCallback, useEffect, useMemo, useState } from 'react'
import EditTaskModal from './components/EditTaskModal'
import TaskColumn from './components/TaskColumn'
import TaskComposer from './components/TaskComposer'
import { createTask, deleteTask, fetchTasks, updateTask, updateTaskStatus } from './services/tasks'

const STATUS_GROUPS = [
  { key: 'todo',        title: 'Planned',   accent: '#ff8f6f' },
  { key: 'in_progress', title: 'In Motion', accent: '#f5b85d' },
  { key: 'done',        title: 'Delivered', accent: '#56bf8c' },
]

const STATUS_TABS    = ['all', 'todo', 'in_progress', 'done']
const PRIORITY_TABS  = ['all', 'high', 'medium', 'low']

function tabLabel(value, type) {
  if (value === 'all') return 'All'
  if (value === 'in_progress') return 'In Progress'
  return value.charAt(0).toUpperCase() + value.slice(1)
}

function App() {
  const [tasks, setTasks]               = useState([])
  const [loading, setLoading]           = useState(true)
  const [submitting, setSubmitting]     = useState(false)
  const [saving, setSaving]             = useState(false)
  const [error, setError]               = useState('')
  const [success, setSuccess]           = useState('')
  const [editingTask, setEditingTask]   = useState(null)
  const [search, setSearch]             = useState('')
  const [statusFilter, setStatusFilter] = useState('all')
  const [priorityFilter, setPriorityFilter] = useState('all')
  const [totalCount, setTotalCount]     = useState(0)

  const loadTasks = useCallback(async () => {
    setLoading(true)
    setError('')
    try {
      // Load all tasks for the board; server-side filters handled as needed
      const data = await fetchTasks({ size: 100 })
      setTasks(data.items)
      setTotalCount(data.total)
    } catch {
      setError('Unable to reach the Task Tracker API. Make sure the backend is running.')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { void loadTasks() }, [loadTasks])

  // Auto-clear banners after 3 s
  useEffect(() => {
    if (!success && !error) return
    const t = setTimeout(() => { setSuccess(''); setError('') }, 3000)
    return () => clearTimeout(t)
  }, [success, error])

  async function handleCreate(payload) {
    setSubmitting(true)
    setError('')
    setSuccess('')
    try {
      const created = await createTask(payload)
      setTasks((cur) => [...cur, created])
      setTotalCount((n) => n + 1)
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
      setTasks((cur) => cur.map((t) => (t.id === taskId ? updated : t)))
      setSuccess('Status updated.')
    } catch {
      setError('Status update failed. Please retry.')
    }
  }

  async function handleDelete(taskId) {
    setError('')
    setSuccess('')
    try {
      await deleteTask(taskId)
      setTasks((cur) => cur.filter((t) => t.id !== taskId))
      setTotalCount((n) => n - 1)
      setSuccess('Task deleted.')
    } catch {
      setError('Delete failed. Please retry.')
    }
  }

  async function handleUpdate(taskId, payload) {
    setSaving(true)
    setError('')
    setSuccess('')
    try {
      const updated = await updateTask(taskId, payload)
      setTasks((cur) => cur.map((t) => (t.id === taskId ? updated : t)))
      setSuccess('Task updated.')
      setEditingTask(null)
    } catch {
      setError('Update failed. Please retry.')
    } finally {
      setSaving(false)
    }
  }

  const stats = useMemo(() => {
    const total      = tasks.length
    const done       = tasks.filter((t) => t.status === 'done').length
    const inProgress = tasks.filter((t) => t.status === 'in_progress').length
    const completion = total === 0 ? 0 : Math.round((done / total) * 100)
    return { total, done, inProgress, completion }
  }, [tasks])

  // Client-side filtering (search + status + priority)
  const filteredTasks = useMemo(() => {
    const q = search.trim().toLowerCase()
    return tasks.filter((t) => {
      const matchSearch   = !q || t.title.toLowerCase().includes(q) || t.description.toLowerCase().includes(q)
      const matchStatus   = statusFilter   === 'all' || t.status   === statusFilter
      const matchPriority = priorityFilter === 'all' || t.priority === priorityFilter
      return matchSearch && matchStatus && matchPriority
    })
  }, [tasks, search, statusFilter, priorityFilter])

  return (
    <div className="app-shell">
      <div className="background-layer" />
      <main className="app-content">

        {/* ── Header ── */}
        <header className="hero">
          <div className="hero-copy">
            <p className="eyebrow">Task Tracker Pro</p>
            <h1>Free tooling, premium execution.</h1>
            <p>
              A full-stack Kanban board powered by FastAPI + Supabase. Create tasks,
              set priority, move them across stages, and edit on the fly.
            </p>
          </div>
          <div className="stats-grid">
            <article>
              <span><ListTodo size={16} /> Total Tasks</span>
              <strong>{stats.total}</strong>
            </article>
            <article>
              <span><Timer size={16} /> In Motion</span>
              <strong>{stats.inProgress}</strong>
            </article>
            <article>
              <span><CheckCircle2 size={16} /> Completion</span>
              <strong>{stats.completion}%</strong>
              <div className="progress-bar">
                <div className="progress-fill" style={{ width: `${stats.completion}%` }} />
              </div>
            </article>
          </div>
        </header>

        {/* ── Workspace ── */}
        <section className="workspace">
          <TaskComposer onCreate={handleCreate} isSubmitting={submitting} />

          {/* Filter bar */}
          <div className="filter-bar">
            {/* Search */}
            <div className="search-wrap">
              <Search size={15} className="search-icon" />
              <input
                id="task-search"
                type="text"
                className="search-input"
                placeholder="Search tasks…"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
              {search && (
                <button className="search-clear" type="button" onClick={() => setSearch('')} aria-label="Clear search">
                  <X size={14} />
                </button>
              )}
            </div>

            {/* Status tabs */}
            <div className="filter-group">
              <span className="filter-label">Status</span>
              <div className="tab-group">
                {STATUS_TABS.map((s) => (
                  <button
                    key={s}
                    type="button"
                    className={`tab-btn${statusFilter === s ? ' active' : ''}`}
                    onClick={() => setStatusFilter(s)}
                  >
                    {tabLabel(s)}
                  </button>
                ))}
              </div>
            </div>

            {/* Priority tabs */}
            <div className="filter-group">
              <span className="filter-label">Priority</span>
              <div className="tab-group">
                {PRIORITY_TABS.map((p) => (
                  <button
                    key={p}
                    type="button"
                    className={`tab-btn tab-btn--${p}${priorityFilter === p ? ' active' : ''}`}
                    onClick={() => setPriorityFilter(p)}
                  >
                    {tabLabel(p)}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Banners */}
          {error   && <div className="banner error"><AlertTriangle size={16} /> {error}</div>}
          {success && <div className="banner success">{success}</div>}

          {/* Board */}
          {loading ? (
            <div className="loading">
              <span className="loading-spinner" />
              Loading tasks…
            </div>
          ) : (
            <div className="board">
              {STATUS_GROUPS.map((group) => (
                <TaskColumn
                  key={group.key}
                  title={group.title}
                  accent={group.accent}
                  tasks={filteredTasks.filter((t) => t.status === group.key)}
                  onStatusChange={handleStatusChange}
                  onDelete={handleDelete}
                  onEdit={setEditingTask}
                />
              ))}
            </div>
          )}
        </section>
      </main>

      {/* Edit modal */}
      {editingTask && (
        <EditTaskModal
          task={editingTask}
          onSave={handleUpdate}
          onClose={() => setEditingTask(null)}
          isSaving={saving}
        />
      )}
    </div>
  )
}

export default App
