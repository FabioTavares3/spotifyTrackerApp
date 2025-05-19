document.getElementById("tracks-btn").addEventListener("click", function(e) {
  e.preventDefault();
  fetch('/api/top_tracks')
    .then(response => response.json())
    .then(data => {
      const section = document.getElementById("tracks");
      section.innerHTML = createTable(data);
    });
});

document.getElementById("artists-btn").addEventListener("click", function(e) {
  e.preventDefault();
  fetch('/api/top_artists')
    .then(response => response.json())
    .then(data => {
      const section = document.getElementById("tracks");
      section.innerHTML = createTable(data);
    });
});

function createTable(data) {
  if (data.length === 0) return "<p>No data available</p>";

  let html = "<table><tr>";
  Object.keys(data[0]).forEach(key => html += `<th>${key}</th>`);
  html += "</tr>";

  data.forEach(row => {
    html += "<tr>";
    Object.values(row).forEach(value => html += `<td>${value}</td>`);
    html += "</tr>";
  });

  html += "</table>";
  return html;
}