function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

let botoesCancelar = document.querySelectorAll(".btn-secondary");
botoesCancelar.forEach((botao) => { 
    botao.addEventListener("click", function (e) {
        const csrftoken = getCookie('csrftoken');
        let pedidoId = e.target.dataset.pedidoId;
        // Faz a requisição para o backend
        // fetch(url, {
        //     method: 'POST',
        //     headers: {
        //         'Content-Type': 'application/json',
        //         'X-CSRFToken': csrftoken,
        //     },
        //     body: JSON.stringify({'pedido_id': pedidoId})
        // })
        // .then(response => response.json())
        // .then(data => {
        //     if (data.sucesso) {
        //         botaoAdicionar.classList.add("oculto");
        //         botaoRemover.classList.remove("oculto");

        //         // 2. Atualiza o ícone do carrinho no cabeçalho (se houver um contador)
        //         const contador = document.getElementById('contagem-cesta');
        //         if (contador) {
        //             contador.innerText = data.novo_total_itens;
        //         }
        //     } else {
        //         alert('Erro ao adicionar: ' + data.erro);
        //         window.location.href = '/login';
        //     }
        // })
        // .catch(error => console.error('Erro:', error));
    });
});