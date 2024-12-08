function salvarQuadras() {
    const pontos = JSON.parse(localStorage.getItem('pontosMarcados')) || [];
  
    if (pontos.length === 0) {
      console.log("Nenhuma quadra para salvar.");
      return;
    }
  
    fetch('/salvar-quadra/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken(), // Inclua o token CSRF
      },
      body: JSON.stringify({ pontos: pontos }),
    })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          console.log(data.message);
          // Opcional: Limpar o localStorage após salvar
          localStorage.removeItem('pontosMarcados');
        } else {
          console.error(data.error || "Erro ao salvar quadras.");
        }
      })
      .catch(error => console.error("Erro na requisição:", error));
  }
  
  // Função para obter o CSRF Token
  function getCSRFToken() {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      if (cookie.trim().startsWith('csrftoken=')) {
        return cookie.trim().split('=')[1];
      }
    }
    return '';
  }
  