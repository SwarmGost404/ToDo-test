export interface Task {
  id: string
  title: string
  description: string
  status: 'todo' | 'in-progress' | 'done'
  createdAt: string | number
}

export interface Column {
  title: string
  status: Task['status']
}