import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import SearchBar from '../components/SearchBar'
import PaperCard from '../components/PaperCard'

function Home() {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  const [recommendations, setRecommendations] = useState([])
  const [recommendationsLoading, setRecommendationsLoading] = useState(false)
  const [recommendationsLoaded, setRecommendationsLoaded] = useState(false)
  const [recommendationsError, setRecommendationsError] = useState('')

  const navigate = useNavigate()

  useEffect(() => {
    const token = localStorage.getItem('access_token')

    if (!token) {
      setLoading(false)
      return
    }

    const getCurrentUser = async () => {
      try {
        const response = await fetch(
          'http://127.0.0.1:8002/api/auth/me',
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        )

        if (!response.ok) {
          localStorage.removeItem('access_token')
          setLoading(false)
          return
        }

        const data = await response.json()
        setUser(data)
      } catch (error) {
        console.error('Unable to verify user:', error)
      } finally {
        setLoading(false)
      }
    }

    getCurrentUser()
  }, [])

  const loadRecommendations = async () => {
    const token = localStorage.getItem('access_token')

    if (!token) {
      navigate('/login')
      return
    }

    setRecommendationsLoading(true)
    setRecommendationsError('')

    try {
      const response = await fetch(
        'http://127.0.0.1:8002/api/recommendations',
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )

      if (!response.ok) {
        throw new Error('Failed to load recommendations')
      }

      const data = await response.json()

      setRecommendations(data)
      setRecommendationsLoaded(true)
    } catch (error) {
      console.error('Unable to load recommendations:', error)

      setRecommendationsError(
        'Unable to load recommendations.'
      )
    } finally {
      setRecommendationsLoading(false)
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('access_token')
    setUser(null)
    setRecommendations([])
    setRecommendationsLoaded(false)
  }

  if (loading) {
    return <p>Loading...</p>
  }

  return (
    <div>
      <h1>Paper Recommender</h1>

      {user ? (
        <div>
          <p>Welcome back!</p>

          <button onClick={handleLogout}>
            Logout
          </button>

          <button onClick={loadRecommendations}>
            Load Recommended Papers
          </button>

          {recommendationsLoading && (
            <p>Loading recommendations...</p>
          )}

          {recommendationsError && (
            <p>{recommendationsError}</p>
          )}

          {recommendationsLoaded &&
            !recommendationsLoading &&
            !recommendationsError && (
              <div>
                <h2>Recommended Papers</h2>

                {recommendations.length === 0 ? (
                  <p>
                    Interact with some papers to start
                    receiving personalized recommendations.
                  </p>
                ) : (
                  recommendations.map((recommendation) => (
                    <PaperCard
                      key={recommendation.paper.arxiv_id}
                      paper={recommendation.paper}
                    />
                  ))
                )}
              </div>
            )}
        </div>
      ) : (
        <div>
          <button onClick={() => navigate('/login')}>
            Login
          </button>

          <button onClick={() => navigate('/register')}>
            Create Account
          </button>
        </div>
      )}

      <p>
        Search for research papers using the search bar below.
      </p>

      <SearchBar />
    </div>
  )
}

export default Home
