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

document.querySelector(".info-produto").addEventListener("click", function(e) {
    const botaoAdicionar = document.querySelector("#btn-adicionar-cesta");
    const botaoRemover = document.querySelector("#btn-retirar-cesta");

    if(e.target.closest("#btn-adicionar-cesta")) {
        let botaoClicado = e.target.closest("#btn-adicionar-cesta");
        const produtoId = botaoClicado.dataset.produtoId;
        const url = "/cesta/adicionar";

        const csrftoken = getCookie('csrftoken');

        // Faz a requisição para o backend
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({'produto_id': produtoId})
        })
        .then(response => response.json())
        .then(data => {
            if (data.sucesso) {
                botaoAdicionar.classList.add("oculto");
                botaoRemover.classList.remove("oculto");

                // 2. Atualiza o ícone do carrinho no cabeçalho (se houver um contador)
                const contador = document.getElementById('contagem-cesta');
                if (contador) {
                    contador.innerText = data.novo_total_itens;
                }
            } else {
                alert('Erro ao adicionar: ' + data.erro);
            }
        })
        .catch(error => console.error('Erro:', error));
    }

    if(e.target.closest("#btn-retirar-cesta")) {
        let botaoClicado = e.target.closest("#btn-retirar-cesta");
        const produtoId = botaoClicado.dataset.produtoId;
        const url = '/cesta/remover';

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'), // Mesma função getCookie usada antes
            },
            body: JSON.stringify({'produto_id': produtoId})
        })
        .then(response => response.json())
        .then(data => {
            if (data.sucesso) {
                document.querySelector("#btn-adicionar-cesta").classList.remove("oculto");
                document.querySelector("#btn-retirar-cesta").classList.add("oculto");
                
                // Atualiza o contador do topo
                document.getElementById('contagem-cesta').innerText = data.novo_total_itens;
            } else {
                alert('Erro ao remover: ' + data.erro);
            }
        });
    }
});