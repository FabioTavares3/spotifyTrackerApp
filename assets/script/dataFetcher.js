// Aguarda o carregamento completo do DOM antes de executar o script
document.addEventListener("DOMContentLoaded", () => {
  // Detecta a página e define o endpoint e o título
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

  // Seleciona a seção onde os dados serão exibidos
  const section = document.getElementById("tracks");

  // Busca e exibe os dados automaticamente ao carregar a página
  fetch(endpoint)
    .then((res) => res.json())
    .then((data) => {
      section.innerHTML = createTable(data);
    });

  // Função para criar uma tabela HTML a partir dos dados recebidos
  function createTable(data) {
    // Caso não haja dados, exibe mensagem
    if (!data.length) return "<p>No data available</p>";

    // Cria o cabeçalho da tabela com as chaves do primeiro objeto
    let html = "<table><tr>";
    Object.keys(data[0]).forEach((key) => (html += `<th>${key}</th>`));
    html += "</tr>";

    // Cria as linhas da tabela com os valores de cada objeto
    data.forEach((row) => {
      html += "<tr>";
      Object.values(row).forEach((value) => (html += `<td>${value}</td>`));
      html += "</tr>";
    });

    html += "</table>";
    return html;
  }
});
