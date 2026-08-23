import { recordInteraction } from "../api";
import "../PaperCard.css";

function PaperCard({ paper }) {

  const handleInteraction = async (interactionType) => {
    try {
      await recordInteraction(
        paper.arxiv_id,
        interactionType
      );
    } catch (error) {
      console.error("Failed to record interaction:", error);
    }
  };

  const handlePdfOpen = async () => {
    try {
      await recordInteraction(
        paper.arxiv_id,
        "pdf_opened"
      );
    } catch (error) {
      console.error("Failed to record PDF interaction:", error);
    }

    window.open(paper.pdf_url, "_blank");
  };

  return (
    <article className="paper-card">

      <div className="paper-card-header">
        <h2 className="paper-title">
          {paper.title}
        </h2>

        <p className="paper-authors">
          {paper.authors.join(", ")}
        </p>
      </div>

      <div className="paper-metadata">

        {paper.published_at && (
          <span>
            Published:{" "}
            {new Date(paper.published_at).toLocaleDateString()}
          </span>
        )}

        <div className="paper-categories">
          {paper.categories.map((category) => (
            <span
              key={category}
              className="paper-category"
            >
              {category}
            </span>
          ))}
        </div>

      </div>

      <div className="paper-abstract">
        <h3>Abstract</h3>
        <p>{paper.abstract}</p>
      </div>

      <div className="paper-actions">

        <div className="interaction-buttons">

          <button
            onClick={() => handleInteraction("liked")}
            aria-label="Like paper"
          >
            👍
          </button>

          <button
            onClick={() => handleInteraction("disliked")}
            aria-label="Dislike paper"
          >
            👎
          </button>

          <button
            onClick={() => handleInteraction("saved")}
          >
            Save
          </button>

        </div>

        <button
          className="pdf-button"
          onClick={handlePdfOpen}
        >
          Open PDF
        </button>

      </div>

    </article>
  );
}

export default PaperCard;