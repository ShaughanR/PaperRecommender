import { recordInteraction } from "../api";

function PaperCard({ paper }) {

  const handleInteraction = async (interactionType) => {
    try {
      await recordInteraction(
        paper.arxiv_id,
        interactionType
      );
    }
    catch (error) {
      console.error("Failed to record interaction:", error);
    }
  };

  const handlePdfOpen = async () => {
    try {
      await recordInteraction(
        paper.arxiv_id,
        "pdf_opened"
      );
    }
    catch (error) {
      console.error("Failed to record PDF interaction:", error);
    }

    window.open(paper.pdf_url, "_blank");
  };

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

      <p>
        <strong>Abstract:</strong>{' '}
        {paper.abstract}
      </p>

      <div>
        <button onClick={() => handleInteraction("liked")}>
          👍
        </button>

        <button onClick={() => handleInteraction("disliked")}>
          👎
        </button>

        <button onClick={() => handleInteraction("saved")}>
          Save
        </button>

        <button onClick={handlePdfOpen}>
          Open PDF
        </button>
      </div>
    </div>
  );
}

export default PaperCard;