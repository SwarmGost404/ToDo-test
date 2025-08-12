export interface Task {
  id: string
  title: string
  description: string
  status: 'todo' | 'in-progress' | 'done'
  color: 'status-red' | 'status-green' | 'status-yellow' | 'none-status'
  createdAt: string | number
}

export interface Column {
  title: string
  status: Task['status']
}