import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

function SearchBar() {
  const [query, setQuery] = useState('')
  const [publishedAfter, setPublishedAfter] = useState('')
  const [publishedBefore, setPublishedBefore] = useState('')

  const navigate = useNavigate()

  function handleSubmit(event) {
    event.preventDefault()

    const params = new URLSearchParams()

    if (query.trim()) {
      params.append('query', query.trim())
    }

    if (publishedAfter) {
      params.append('published_after', publishedAfter)
    }

    if (publishedBefore) {
      params.append('published_before', publishedBefore)
    }

    navigate(`/search?${params.toString()}`)
  }

  return (
    <form onSubmit={handleSubmit}>

      <div>
        <label>Search:</label>
        <input
          type="text"
          placeholder="Search papers..."
          value={query}
          onChange={event => setQuery(event.target.value)}
        />
      </div>

      <div>
        <label>Published after:</label>
        <input
          type="date"
          value={publishedAfter}
          onChange={event => setPublishedAfter(event.target.value)}
        />
      </div>

      <div>
        <label>Published before:</label>
        <input
          type="date"
          value={publishedBefore}
          onChange={event => setPublishedBefore(event.target.value)}
        />
      </div>

      <button type="submit">
        Search
      </button>

    </form>
  )
}

export default SearchBar