import { VFC } from 'react'
// import logo from './logo.svg'
import Container from '@mui/material/Container'
import Typography from '@mui/material/Typography'
import Box from '@mui/material/Box'
import Button from '@mui/material/Button'
import Link from '@mui/material/Link'
import ProTip from './ProTip'
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

const App: VFC = () => (
  <Container maxWidth="sm">
    <Box sx={{ my: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        React App with TypeScript
      </Typography>
      <ProTip />
      <Button variant="contained">Hello World</Button>
      <Copyright />
    </Box>
  </Container>
)

export default App
