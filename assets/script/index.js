// Fetch data from the '/top-tracks' endpoint
fetch('/top-tracks')
  .then(res => {
    // Check if the response is successful
    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }
    return res.json(); // Parse the response as JSON
  })
  .then(tracks => {
    // Get the container element where the cards will be displayed
    const container = document.getElementById('tracks');

    // Iterate over the tracks and create a card for each one
    tracks.forEach(track => {
      const card = document.createElement('div'); // Create a new div element
      card.className = 'card'; // Add the 'card' class for styling

      // Set the inner HTML of the card with track details
      card.innerHTML = `
        <img src="${track.song_image}" alt="${track.song_name}" />
        <h3>${track.song_name}</h3>
        <p><strong>Album:</strong> ${track.album_name}</p>
        <p><strong>Minutes Listened:</strong> ${track.estimated_total_minutes}</p>
        <a href="${track.song_url}" target="_blank">Listen on Spotify</a>
      `;

      // Append the card to the container
      container.appendChild(card);
    });
  })
  .catch(error => {
    // Log any errors that occur during the fetch or processing
    console.error('Error fetching top tracks:', error);
  });