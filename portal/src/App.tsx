import { VFC } from 'react'
import { DataGrid, GridColDef } from '@mui/x-data-grid'
import Container from '@mui/material/Container'
import Typography from '@mui/material/Typography'
import Box from '@mui/material/Box'
import Button from '@mui/material/Button'
// import Link from '@mui/material/Link'
import './App.css'

const Copyright = () => (
  <Typography variant="body2" color="text.secondary" align="center">
    {'Copyright © Tech Meetup-Kinsol '}
    {/* <Link color="inherit" href="https://mui.com/">
      Tech Meetup-Kinsol
    </Link>{' '} */}
    {new Date().getFullYear()}.
  </Typography>
)

const columns: GridColDef[] = [
  { field: 'id', headerName: 'ID', width: 70 },
  { field: 'task_name', headerName: 'コンテンツ名', width: 200 },
  { field: 'scheduled_at', headerName: '通知時刻', width: 200 },
]

const rows = [
  { id: 1, user_id: 'aaa', task_name: 'twitter', scheduled_at: '08:00:00' },
  { id: 2, user_id: 'bbb', task_name: 'twitter', scheduled_at: '18:00:00' },
]

const DataTable = () => (
  <div style={{ height: 400, width: '100%' }}>
    <DataGrid rows={rows} columns={columns} pageSize={5} rowsPerPageOptions={[5]} checkboxSelection />
  </div>
)

const App: VFC = () => (
  <Container maxWidth="sm">
    <Box sx={{ my: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        React App with TypeScript
      </Typography>
      <DataTable />
      <Button variant="contained">Hello World</Button>
      <Copyright />
    </Box>
  </Container>
)

export default App
