// Aguarda o carregamento completo do DOM antes de executar o script
document.addEventListener("DOMContentLoaded", () => {
  // Seleciona os botões e a seção onde os dados serão exibidos
  const tracksBtn = document.getElementById("tracks-btn");
  const artistsBtn = document.getElementById("artists-btn");
  const section = document.getElementById("tracks");

  // Evento para buscar e exibir as faixas mais ouvidas
  tracksBtn.addEventListener("click", (e) => {
    e.preventDefault();
    // Faz uma requisição para a rota de top tracks
    fetch("/api/top_tracks")
      .then((res) => res.json())
      .then((data) => {
        // Atualiza a seção com a tabela gerada
        section.innerHTML = createTable(data);
      });
  });

  // Evento para buscar e exibir os artistas mais ouvidos
  artistsBtn.addEventListener("click", (e) => {
    e.preventDefault();
    // Faz uma requisição para a rota de top artists
    fetch("/api/top_artists")
      .then((res) => res.json())
      .then((data) => {
        // Atualiza a seção com a tabela gerada
        section.innerHTML = createTable(data);
      });
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
