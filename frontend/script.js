document.getElementById("recommendation-form").addEventListener("submit", function(event) {
    event.preventDefault();

    const userId = document.getElementById("user_id").value;
    const n = document.getElementById("n").value;

    fetch(`/recommend?user_id=${userId}&n=${n}`)
        .then(response => response.json())
        .then(data => {
            const recommendationsDiv = document.getElementById("recommendations");
            recommendationsDiv.innerHTML = ''; // Clear previous recommendations
            data.recommendations.forEach(item => {
                const artistElement = document.createElement("div");
                artistElement.textContent = `${item.artist}: ${item.score}`;
                recommendationsDiv.appendChild(artistElement);
            });
        })
        .catch(error => {
            console.error("Error fetching recommendations:", error);
        });
})
