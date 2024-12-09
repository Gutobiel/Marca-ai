document.addEventListener("DOMContentLoaded", () => {
    const coordenadasIniciais = [-15.7801, -47.9292];
  
    // Inicializa o mapa
    const map = L.map("map").setView(coordenadasIniciais, 14);
  
    // Adiciona o mapa base do OpenStreetMap
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
    }).addTo(map);
  
    // Função para carregar marcadores do banco de dados
    async function carregarMarcadores() {
      try {
        const response = await fetch(listarPontosUrl); // Usa a variável de URL definida no HTML
        const pontos = await response.json();
  
        pontos.forEach((ponto) => {
          const marker = L.marker([ponto.lat, ponto.lng]).addTo(map);
          marker.bindPopup(`
            <h3>${ponto.nome}</h3>
            <p>${ponto.descricao}</p>
          `);
        });
      } catch (error) {
        console.error("Erro ao carregar pontos:", error);
      }
    }
  
    // Carrega marcadores ao iniciar
    carregarMarcadores();
  
    // Adiciona marcador ao clicar no mapa
    map.on("click", (e) => {
      const { lat, lng } = e.latlng;
  
      // Adiciona marcador
      const marker = L.marker([lat, lng]).addTo(map);
  
      // Adiciona popup com formulário
      marker.bindPopup(`
        <div>
          <h3>Definir o Ponto</h3>
          <form id="form-ponto" onsubmit="salvarPonto(event, ${lat}, ${lng})">
            <label for="nome-ponto">Nome:</label>
            <input type="text" id="nome-ponto" required>
            <label for="descricao-ponto">Descrição:</label>
            <textarea id="descricao-ponto" required></textarea>
            <button type="submit">Salvar</button>
          </form>
        </div>
      `).openPopup();
    });
  
    // Função para salvar o ponto
    async function salvarPonto(event, lat, lng) {
      event.preventDefault();  // Evita que o formulário envie a requisição de forma tradicional
  
      const nome = document.getElementById("nome-ponto").value;
      const descricao = document.getElementById("descricao-ponto").value;
  
      const dados = { lat, lng, nome, descricao };
  
      try {
        const response = await fetch("{% url 'salvar_ponto' %}", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": "{{ csrf_token }}", // Necessário para a proteção CSRF
          },
          body: JSON.stringify(dados),
        });
  
        if (response.ok) {
          alert("Ponto salvo com sucesso!");
          // Após salvar, recarregue os marcadores
          carregarMarcadores();
        } else {
          alert("Erro ao salvar o ponto!");
        }
      } catch (error) {
        console.error("Erro:", error);
        alert("Erro ao salvar o ponto!");
      }
    }

    async function carregarMarcadores() {
        try {
          const response = await fetch(listarPontosUrl);  // URL para listar os pontos
          const pontos = await response.json();
      
          pontos.forEach((ponto) => {
            const marker = L.marker([ponto.lat, ponto.lng]).addTo(map);
            marker.bindPopup(`
              <h3>${ponto.nome}</h3>
              <p>${ponto.descricao}</p>
            `);
          });
        } catch (error) {
          console.error("Erro ao carregar pontos:", error);
        }
      }
      
  });
  