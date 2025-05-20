// Aguarda o carregamento completo do DOM antes de executar o script
document.addEventListener("DOMContentLoaded", () => {
  // Detecta a página e define o endpoint
  let endpoint = "";
  if (window.location.pathname.includes("artists.html")) {
    endpoint = "/api/top_artists";
  } else if (window.location.pathname.includes("albums.html")) {
    endpoint = "/api/top_albums";
  } else if (window.location.pathname.includes("history.html")) {
    endpoint = "/api/listening_history";
  } else {
    endpoint = "/api/top_tracks";
  }

  const section = document.getElementById("tracks");

  // Cria botão de alternância
  const toggleBtn = document.createElement("button");
  toggleBtn.textContent = "Ver como Tabela";
  toggleBtn.style.marginBottom = "1rem";
  let showTable = false;
  section.parentNode.insertBefore(toggleBtn, section);

  let lastData = [];

  // Busca e exibe os dados automaticamente ao carregar a página
  fetch(endpoint)
    .then((res) => res.json())
    .then((data) => {
      lastData = data;
      section.innerHTML = createCards(data);
    });

  toggleBtn.addEventListener("click", () => {
    showTable = !showTable;
    toggleBtn.textContent = showTable ? "Ver como Cards" : "Ver como Tabela";
    section.innerHTML = showTable
      ? createTable(lastData)
      : createCards(lastData);
  });

  // Função para criar cards HTML a partir dos dados recebidos
  function createCards(data) {
    if (!data.length) return "<p>Nenhum dado disponível</p>";

    if (endpoint === "/api/top_tracks") {
      return data
        .map(
          (track) => `
        <div class="card">
          <img src="${track.song_image}" alt="${track.song_name}" />
          <h3>${track.song_name}</h3>
          <p><strong>Álbum:</strong> ${track.album_name}</p>
          <p><strong>Minutos Ouvidos:</strong> ${track.estimated_total_minutes}</p>
          <a href="${track.song_url}" target="_blank">Ouvir no Spotify</a>
        </div>
      `
        )
        .join("");
    }
    if (endpoint === "/api/top_artists") {
      return data
        .map(
          (artist) => `
        <div class="card">
          <img src="${artist.artist_image}" alt="${artist.artist_name}" />
          <h3>${artist.artist_name}</h3>
          <p><strong>Mês:</strong> ${artist.month}</p>
          <p><strong>Minutos Ouvidos:</strong> ${artist.estimated_total_minutes}</p>
          <a href="${artist.artist_url}" target="_blank">Ver no Spotify</a>
        </div>
      `
        )
        .join("");
    }
    if (endpoint === "/api/top_albums") {
      return data
        .map(
          (album) => `
        <div class="card">
          <img src="${album.album_image}" alt="${album.album_name}" />
          <h3>${album.album_name}</h3>
          <p><strong>Mês:</strong> ${album.month}</p>
          <p><strong>Minutos Ouvidos:</strong> ${album.estimated_total_minutes}</p>
          <a href="${album.album_url}" target="_blank">Ver no Spotify</a>
        </div>
      `
        )
        .join("");
    }
    if (endpoint === "/api/listening_history") {
      return data
        .map(
          (item) => `
        <div class="card">
          <img src="${item.song_image}" alt="${item.song_name}" />
          <h3>${item.song_name}</h3>
          <p><strong>Artista:</strong> ${item.artist_name}</p>
          <p><strong>Álbum:</strong> ${item.album_name}</p>
          <p><strong>Data:</strong> ${item.timestamp}</p>
        </div>
      `
        )
        .join("");
    }
    // fallback
    return "<p>Nenhum dado disponível</p>";
  }

  // Função para criar tabela HTML a partir dos dados recebidos
  function createTable(data) {
    if (!data.length) return "<p>Nenhum dado disponível</p>";

    let html = "<table><tr>";
    Object.keys(data[0]).forEach((key) => (html += `<th>${key}</th>`));
    html += "</tr>";

    data.forEach((row) => {
      html += "<tr>";
      Object.values(row).forEach((value) => (html += `<td>${value}</td>`));
      html += "</tr>";
    });

    html += "</table>";
    return html;
  }
});
