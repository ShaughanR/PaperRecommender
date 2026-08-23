import { useEffect, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import PaperCard from '../components/PaperCard'
import SearchBar from '../components/SearchBar'

function SearchResults() {
  const [searchParams] = useSearchParams()

  const query = searchParams.get('query')

  const publishedAfter =
    searchParams.get('published_after')

  const publishedBefore =
    searchParams.get('published_before')

  const pageSize = parseInt(
    searchParams.get('page_size') || '20',
    10
  )

  const [papers, setPapers] = useState([])

  const [loading, setLoading] = useState(true)

  const [loadingMore, setLoadingMore] = useState(false)

  const [error, setError] = useState(null)

  // ---------------------------------------------------------
  // Current search state
  //
  // arxivStart represents the next position that should be
  // requested from arXiv when "Load More" is clicked.
  // ---------------------------------------------------------

  const [searchState, setSearchState] = useState({
    arxivStart: 0
  })

  // ---------------------------------------------------------
  // Initial search
  // ---------------------------------------------------------

  useEffect(() => {

    if (!query) {

      setPapers([])

      setSearchState({
        arxivStart: 0
      })

      setLoading(false)

      return
    }

    setLoading(true)
    setError(null)

    // -------------------------------------------------------
    // A new search has started.
    //
    // Always begin arXiv from position 0.
    // -------------------------------------------------------

    setSearchState({
      arxivStart: 0
    })

    const searchParameters =
      new URLSearchParams()

    searchParameters.append(
      'query',
      query
    )

    if (publishedAfter) {

      searchParameters.append(
        'published_after',
        publishedAfter
      )
    }

    if (publishedBefore) {

      searchParameters.append(
        'published_before',
        publishedBefore
      )
    }

    searchParameters.append(
      'page_size',
      pageSize.toString()
    )

    // -------------------------------------------------------
    // Initial searches always start at arXiv position 0.
    // -------------------------------------------------------

    searchParameters.append(
      'arxiv_start',
      '0'
    )

    const url =
      `http://127.0.0.1:8003/api/papers/search?${searchParameters.toString()}`

    console.log(
      'INITIAL SEARCH:',
      url
    )

    fetch(url)

      .then(response => {

        if (!response.ok) {

          throw new Error(
            'Failed to search papers'
          )
        }

        return response.json()
      })

      .then(data => {

        console.log(
          'INITIAL SEARCH RESULTS:',
          data.papers.length
        )

        console.log(
          'NEXT ARXIV START:',
          data.next_arxiv_start
        )

        // ---------------------------------------------------
        // Store the papers returned by the backend.
        // ---------------------------------------------------

        setPapers(
          data.papers
        )

        // ---------------------------------------------------
        // Store the next arXiv position.
        //
        // This is what Load More will use.
        // ---------------------------------------------------

        setSearchState({
          arxivStart:
            data.next_arxiv_start
        })

        setLoading(false)
      })

      .catch(error => {

        console.error(
          'Search failed:',
          error
        )

        setError(
          error.message
        )

        setLoading(false)
      })

  }, [
    query,
    publishedAfter,
    publishedBefore,
    pageSize
  ])


  // ---------------------------------------------------------
  // Load more results
  // ---------------------------------------------------------

  const loadMore = async () => {

    if (loadingMore) {
      return
    }

    setLoadingMore(true)
    setError(null)

    try {

      const searchParameters =
        new URLSearchParams()

      searchParameters.append(
        'query',
        query
      )

      if (publishedAfter) {

        searchParameters.append(
          'published_after',
          publishedAfter
        )
      }

      if (publishedBefore) {

        searchParameters.append(
          'published_before',
          publishedBefore
        )
      }

      searchParameters.append(
        'page_size',
        pageSize.toString()
      )

      // -----------------------------------------------------
      // IMPORTANT:
      //
      // Use the arXiv position returned by the previous
      // backend request.
      // -----------------------------------------------------

      searchParameters.append(
        'arxiv_start',
        searchState.arxivStart.toString()
      )

      // -----------------------------------------------------
      // Tell the backend which papers have already been
      // displayed so they are not returned again.
      // -----------------------------------------------------

      papers.forEach(paper => {

        searchParameters.append(
          'excluded_paper_ids',
          paper.arxiv_id
        )
      })

      const url =
        `http://127.0.0.1:8003/api/papers/search?${searchParameters.toString()}`

      console.log(
        'LOAD MORE:',
        url
      )

      console.log(
        'CURRENT ARXIV START:',
        searchState.arxivStart
      )

      const response =
        await fetch(url)

      if (!response.ok) {

        throw new Error(
          'Failed to load more papers'
        )
      }

      const data =
        await response.json()

      console.log(
        'LOAD MORE RESULTS:',
        data.papers.length
      )

      console.log(
        'NEXT ARXIV START:',
        data.next_arxiv_start
      )

      // -----------------------------------------------------
      // Add the newly returned papers to the existing papers.
      // -----------------------------------------------------

      setPapers(previousPapers => [
        ...previousPapers,
        ...data.papers
      ])

      // -----------------------------------------------------
      // Update the pagination position.
      //
      // The next Load More request will begin here.
      // -----------------------------------------------------

      setSearchState({
        arxivStart:
          data.next_arxiv_start
      })

    } catch (error) {

      console.error(
        'Failed to load more papers:',
        error
      )

      setError(
        error.message
      )

    } finally {

      setLoadingMore(false)
    }
  }


  return (
    <div className="search-page">

      <header className="search-page-header">

        <h1>
          Search Papers
        </h1>

        <div className="search-container">
          <SearchBar />
        </div>

      </header>


      <main className="search-page-content">

        {!query && (

          <div className="search-status">

            <h2>
              Search for a research paper
            </h2>

            <p>
              Enter a search term above to find
              research papers.
            </p>

          </div>

        )}


        {query && loading && (

          <div className="search-status">

            <h2>
              Searching...
            </h2>

            <p>
              Searching for "{query}"...
            </p>

          </div>

        )}


        {query && error && (

          <div className="search-status search-error">

            <h2>
              Something went wrong
            </h2>

            <p>
              {error}
            </p>

          </div>

        )}


        {query && !loading && !error && (

          <section className="search-results">

            <div className="search-results-header">

              <h2>
                Search Results
              </h2>

              <p>
                Results for:{' '}
                <strong>
                  {query}
                </strong>
              </p>

              <p>
                Showing {papers.length} papers
              </p>

            </div>


            {papers.length === 0 ? (

              <div className="search-status">

                <p>
                  No papers found.
                </p>

              </div>

            ) : (

              <>

                <div className="paper-list">

                  {papers.map(paper => (

                    <PaperCard
                      key={paper.arxiv_id}
                      paper={paper}
                    />

                  ))}

                </div>


                <div className="load-more-container">

                  <button
                    onClick={loadMore}
                    disabled={loadingMore}
                  >

                    {loadingMore
                      ? 'Loading...'
                      : 'Load More'}

                  </button>

                </div>

              </>

            )}

          </section>

        )}

      </main>

    </div>
  )
}

export default SearchResults