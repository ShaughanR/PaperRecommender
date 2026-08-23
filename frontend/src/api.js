const API_URL = "http://127.0.0.1:8003";

export async function getRecommendations(token) {
    const response = await fetch(
        "http://127.0.0.1:8003/api/recommendations",
        {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }
    );

    if (!response.ok) {
        throw new Error("Failed to load recommendations");
    }

    return response.json();
}





export async function recordInteraction(paperId, interactionType) {
  const token = localStorage.getItem("access_token");

  const response = await fetch(
    `${API_URL}/api/users/interactions`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify({
        paper_id: paperId,
        interaction_type: interactionType
      })
    }
  );

  if (!response.ok) {
    const data = await response.json();
    console.error("Interaction API error:", data);

    throw new Error("Failed to record interaction");
  }

  return response.json();
}