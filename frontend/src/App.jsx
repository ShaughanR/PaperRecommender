import { useEffect, useState } from 'react'

function App() {
  const [status, setStatus] = useState('Connecting...')

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/health')
      .then(response => response.json())
      .then(data => {
        setStatus(data.status)
      })
      .catch(() => {
        setStatus('Backend connection failed')
      })
  }, [])

  return (
    <div>
      <h1>Paper Recommender</h1>
      <p>Backend status: {status}</p>
    </div>
  )
}

export default App
