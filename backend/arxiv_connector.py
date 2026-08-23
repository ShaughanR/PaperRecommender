import logging
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from backend.models import Paper


logging.basicConfig(level=logging.DEBUG)


MAX_PAGE_SIZE = 50


def get_base_arxiv_id(entry_id):
    arxiv_id = entry_id.rstrip("/").split("/")[-1]
    return arxiv_id.rsplit("v", 1)[0]


def paper_transformer(result) -> Paper:
    return Paper(
        arxiv_id=get_base_arxiv_id(result.entry_id),
        title=result.title,
        authors=[
            author.name
            for author in result.authors
        ],
        abstract=result.summary,
        published_at=result.published,
        updated_at=result.updated,
        doi=result.doi,
        categories=result.categories,
        pdf_url=result.pdf_url
    )


def search_papers(
    query: str | None,
    max_results: int,
    start: int = 0,
    published_after=None,
    published_before=None
):
    # ---------------------------------------------------------
    # Safety limits
    # ---------------------------------------------------------

    max_results = min(
        max_results,
        MAX_PAGE_SIZE
    )

    max_results = max(
        max_results,
        1
    )

    start = max(
        start,
        0
    )

    # ---------------------------------------------------------
    # Build query
    # ---------------------------------------------------------

    query_parts = []

    if query and query.strip():
        query_parts.append(
            f"all:{query.strip()}"
        )

    if published_after or published_before:
        start_date = (
            published_after.replace("-", "") + "000000"
            if published_after
            else "00000101000000"
        )

        end_date = (
            published_before.replace("-", "") + "235959"
            if published_before
            else "99991231235959"
        )

        query_parts.append(
            f"submittedDate:["
            f"{start_date} TO {end_date}]"
        )

    arxiv_query = " AND ".join(
        query_parts
    )

    # ---------------------------------------------------------
    # Build arXiv API request
    # ---------------------------------------------------------

    params = {
        "search_query": arxiv_query,
        "start": start,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending"
    }

    url = (
        "https://export.arxiv.org/api/query?"
        + urllib.parse.urlencode(params)
    )

    logging.info(
        "Requesting arXiv batch: start=%s, max_results=%s, query=%s",
        start,
        max_results,
        arxiv_query
    )

    # ---------------------------------------------------------
    # Request with retry handling
    # ---------------------------------------------------------

    for attempt in range(3):

        try:

            request = urllib.request.Request(
                url,
                headers={
                    "User-Agent":
                        "PaperRecommender/1.0"
                }
            )

            with urllib.request.urlopen(
                request,
                timeout=30
            ) as response:

                xml_data = response.read()

            break

        except Exception as error:

            logging.warning(
                "arXiv request failed "
                "(attempt %s/3): %s",
                attempt + 1,
                error
            )

            if attempt == 2:
                raise

            time.sleep(5)

    # ---------------------------------------------------------
    # Parse response
    # ---------------------------------------------------------

    root = ET.fromstring(
        xml_data
    )

    namespace = {
        "atom":
            "http://www.w3.org/2005/Atom",
        "arxiv":
            "http://arxiv.org/schemas/atom"
    }

    entries = root.findall(
        "atom:entry",
        namespace
    )

    # ---------------------------------------------------------
    # Convert results into Paper objects
    # ---------------------------------------------------------

    for entry in entries:

        entry_id = entry.find(
            "atom:id",
            namespace
        ).text

        title = entry.find(
            "atom:title",
            namespace
        ).text.strip()

        abstract = entry.find(
            "atom:summary",
            namespace
        ).text.strip()

        published = entry.find(
            "atom:published",
            namespace
        ).text

        updated = entry.find(
            "atom:updated",
            namespace
        ).text

        authors = []

        for author in entry.findall(
            "atom:author",
            namespace
        ):

            name = author.find(
                "atom:name",
                namespace
            )

            if name is not None:
                authors.append(
                    name.text
                )

        categories = []

        for category in entry.findall(
            "atom:category",
            namespace
        ):

            term = category.attrib.get(
                "term"
            )

            if term:
                categories.append(term)

        doi = None

        doi_element = entry.find(
            "arxiv:doi",
            namespace
        )

        if doi_element is not None:
            doi = doi_element.text

        pdf_url = None

        for link in entry.findall(
            "atom:link",
            namespace
        ):

            if link.attrib.get("title") == "pdf":
                pdf_url = link.attrib.get(
                    "href"
                )
                break

        # -----------------------------------------------------
        # Construct Paper
        # -----------------------------------------------------

        from backend.models import Paper

        yield Paper(
            arxiv_id=get_base_arxiv_id(
                entry_id
            ),
            title=title,
            authors=authors,
            abstract=abstract,
            published_at=published,
            updated_at=updated,
            doi=doi,
            categories=categories,
            pdf_url=pdf_url
        )