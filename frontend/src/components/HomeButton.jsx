import { useNavigate } from 'react-router-dom'

function HomeButton() {
  const navigate = useNavigate()

  return (
    <button
      className="home-button"
      onClick={() => navigate('/')}
    >
      <img src="/home-icon.png" alt="Home" />
    </button>
  )
}

export default HomeButton