import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

function SearchBar() {
  const [query, setQuery] = useState('')
  const [publishedAfter, setPublishedAfter] = useState('')
  const [publishedBefore, setPublishedBefore] = useState('')
  const [pageSize, setPageSize] = useState('20')

  const navigate = useNavigate()

  function handleSubmit(event) {
    event.preventDefault()

    const params = new URLSearchParams()

    if (query.trim()) {
      params.append(
        'query',
        query.trim()
      )
    }

    if (publishedAfter) {
      params.append(
        'published_after',
        publishedAfter
      )
    }

    if (publishedBefore) {
      params.append(
        'published_before',
        publishedBefore
      )
    }

    params.append(
      'page_size',
      pageSize
    )

    navigate(
      `/search?${params.toString()}`
    )
  }

  return (
    <form
      className="search-form"
      onSubmit={handleSubmit}
    >

      <div className="search-field">
        <label>
          Search:
        </label>

        <input
          type="text"
          placeholder="Search papers..."
          value={query}
          onChange={event =>
            setQuery(event.target.value)
          }
        />
      </div>

      <div className="search-field">
        <label>
          Published after:
        </label>

        <input
          type="date"
          value={publishedAfter}
          onChange={event =>
            setPublishedAfter(
              event.target.value
            )
          }
        />
      </div>

      <div className="search-field">
        <label>
          Published before:
        </label>

        <input
          type="date"
          value={publishedBefore}
          onChange={event =>
            setPublishedBefore(
              event.target.value
            )
          }
        />
      </div>

      <div className="search-field">
        <label>
          Papers per page:
        </label>

        <select
          value={pageSize}
          onChange={event =>
            setPageSize(
              event.target.value
            )
          }
        >
          <option value="10">
            10
          </option>

          <option value="20">
            20
          </option>

          <option value="30">
            30
          </option>

          <option value="40">
            40
          </option>

          <option value="50">
            50
          </option>
        </select>
      </div>

      <button type="submit">
        Search
      </button>

    </form>
  )
}

export default SearchBar
