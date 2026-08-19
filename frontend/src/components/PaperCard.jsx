function PaperCard({ paper }) {
  return (
    <div className="paper-card">
      <h2>{paper.title}</h2>

      <p>
        <strong>Authors:</strong>{' '}
        {paper.authors.join(', ')}
      </p>

      <p>
        <strong>Categories:</strong>{' '}
        {paper.categories.join(', ')}
      </p>

      <p>{paper.abstract}</p>
    </div>
  )
}

export default PaperCard