import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [message, setMessage] = useState<string>('')
  const [loading, setLoading] = useState<boolean>(true)

  useEffect(() => {
    fetch('http://localhost:8000/api/hello')
      .then(response => response.json())
      .then(data => {
        setMessage(data.message)
        setLoading(false)
      })
      .catch(error => {
        console.error('Error fetching from API:', error)
        setMessage('Error connecting to backend')
        setLoading(false)
      })
  }, [])

  return (
    <div className="App">
      <h1>Hello World from React TypeScript!</h1>
      <div className="card">
        {loading ? (
          <p>Loading from backend...</p>
        ) : (
          <p>Backend says: <strong>{message}</strong></p>
        )}
      </div>
    </div>
  )
}

export default App
