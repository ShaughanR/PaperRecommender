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
          'http://127.0.0.1:8003/api/auth/me',
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
        'http://127.0.0.1:8003/api/recommendations',
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
      <div className="home-page">

        <header className="home-header">
          <h1>Paper Recommender</h1>

          {user ? (
            <div className="user-section">
              <p>Welcome back!</p>

              <button onClick={handleLogout}>
                Logout
              </button>
            </div>
          ) : (
            <div className="auth-section">
              <button onClick={() => navigate('/login')}>
                Login
              </button>

              <button onClick={() => navigate('/register')}>
                Create Account
              </button>
            </div>
          )}
        </header>

        <main className="home-content">

          <section className="search-section">
            <h2>Search Research Papers</h2>

            <div className="search-container">
              <SearchBar />
            </div>
          </section>

          {user && (
            <section className="recommendations-section">

              <div className="recommendations-header">
                <div>
                  <h2>Recommended Papers</h2>
                  <p>
                    Papers selected based on your interactions.
                  </p>
                </div>

                <button onClick={loadRecommendations}>
                  Load Recommendations
                </button>
              </div>

              {recommendationsLoading && (
                <p className="status-message">
                  Loading recommendations...
                </p>
              )}

              {recommendationsError && (
                <p className="error-message">
                  {recommendationsError}
                </p>
              )}

              {recommendationsLoaded &&
                !recommendationsLoading &&
                !recommendationsError && (
                  recommendations.length === 0 ? (
                    <p className="status-message">
                      Interact with some papers to start
                      receiving personalized recommendations.
                    </p>
                  ) : (
                    <div className="paper-list">
                      {recommendations.map((recommendation) => (
                        <PaperCard
                          key={recommendation.paper.arxiv_id}
                          paper={recommendation.paper}
                        />
                      ))}
                    </div>
                  )
                )}

            </section>
          )}

        </main>

      </div>
    )
}

export default Home
