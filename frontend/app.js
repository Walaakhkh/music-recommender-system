document.getElementById('get-recommendations').addEventListener('click', function () {
    const userId = document.getElementById('user-id').value;

    if (!userId) {
        alert('Please enter a user ID!');
        return;
    }

    // Clear previous recommendations
    const recommendationList = document.getElementById('recommendation-list');
    recommendationList.innerHTML = '';

    // Fetch recommendations from the backend
    fetch(`http://localhost:5000/recommend/${userId}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert('Error: ' + data.error);
                return;
            }

            const recommendations = data.recommendations;

            // Display recommendations in the list
            recommendations.forEach(rec => {
                const listItem = document.createElement('li');
                listItem.textContent = `${rec.artist}: Score ${rec.score}`;
                recommendationList.appendChild(listItem);
            });
        })
        .catch(error => {
            console.error('Error fetching recommendations:', error);
            alert('There was an error fetching recommendations. Please try again later.');
        });
});
