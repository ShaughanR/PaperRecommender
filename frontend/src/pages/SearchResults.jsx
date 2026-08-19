import { useEffect, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import PaperCard from '../components/PaperCard'
import SearchBar from '../components/SearchBar'

function SearchResults() {
  const [searchParams] = useSearchParams()
  const query = searchParams.get('query')

  const [papers, setPapers] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (!query) {
      setPapers([])
      setLoading(false)
      return
    }

    setLoading(true)
    setError(null)

    fetch(
      `http://127.0.0.1:8000/api/papers/search?query=${encodeURIComponent(query)}&limit=20`
    )
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to search papers')
        }

        return response.json()
      })
      .then(data => {
        setPapers(data)
        setLoading(false)
      })
      .catch(error => {
        setError(error.message)
        setLoading(false)
      })
  }, [query])

  if (!query) {
    return <h1>Please enter a search query.</h1>
  }

  if (loading) {
    return <h1>Searching for "{query}"...</h1>
  }

  if (error) {
    return <h1>Error: {error}</h1>
  }

  return (
    <div>
      <h1>Search Results</h1>

        <SearchBar />

      <p>
        Results for: <strong>{query}</strong>
      </p>

      {papers.length === 0 ? (
        <p>No papers found.</p>
      ) : (
        papers.map(paper => (
          <PaperCard
            key={paper.arxiv_id}
            paper={paper}
          />
        ))
      )}
    </div>
  )
}

export default SearchResults