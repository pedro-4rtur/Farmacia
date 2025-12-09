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

let botoesQuantidade = document.querySelectorAll(".qty-btn");
botoesQuantidade.forEach((botao) => {
    botao.addEventListener("click", function(e) {
        let inputQuantidade = e.target.closest('.quantity-selector').querySelector(".qty-input");
        let operacao;

        if(botao.dataset.operacao == '-' && Number.parseInt(inputQuantidade.value) > 1) {
            inputQuantidade.value = Number.parseInt(inputQuantidade.value) - 1;
            operacao = 'remover';
        } else if(botao.dataset.operacao == '+' && Number.parseInt(inputQuantidade.value) < Number.parseInt(inputQuantidade.max)){
            inputQuantidade.value = Number.parseInt(inputQuantidade.value) + 1;
            operacao = 'adicionar';
        }

        const produtoId = e.target.closest(".item-controls").querySelector(".remove-btn").dataset.produtoId;

        if(operacao != undefined) {
            const url = `/cesta/${operacao}`;

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
                    precoUnitario = Number.parseFloat(inputQuantidade.dataset.precoUnitario);
                    quantidade = Number.parseInt(inputQuantidade.value);
                    valorTotal = (precoUnitario * quantidade).toFixed(2);

                    saidaTotal = e.target.closest('.cart-item').querySelector(".item-total-price");
                    saidaTotal.innerHTML = `R$ ${valorTotal}`;

                    atualizarSubtotal();
                } else {
                    alert('Erro ao remover: ' + data.erro);
                }
            })
            .catch(error => console.error('Erro:', error));
        }
    })
})

let itens = document.querySelectorAll(".cart-item")
itens.forEach((item) => {
    item.addEventListener("click", function(e) {
        let botaoClicado = e.target.closest('.remove-btn');
        const produtoId = botaoClicado.dataset.produtoId;
        const url = "/cesta/remover";

        const csrftoken = getCookie('csrftoken');

        // Faz a requisição para o backend
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({'produto_id': produtoId, 'delete': true})
        })
        .then(response => response.json())
        .then(data => {
            if (data.sucesso) {
                item.style.display = "none";

                // Atualiza o ícone do carrinho no cabeçalho (se houver um contador)
                const contador = document.getElementById('contagem-cesta');
                if (contador) {
                    contador.innerText = data.novo_total_itens;
                }

                atualizarSubtotal();
            } else {
                alert('Erro ao remover: ' + data.erro);
            }
        })
        .catch(error => console.error('Erro:', error));
    });
})

function atualizarSubtotal() {
    let totais = document.querySelectorAll(".item-total-price");
    let total = 0;
    totais.forEach((totalIndividual) => {
        let valor = totalIndividual.innerHTML.replace(/,/g, '').replace(/[^\d.]/g, '');
        total += parseFloat(valor);
    })
    let subtotal = document.getElementById('subtotal');
    let valorTotal = document.getElementById('valor-total');
    subtotal.innerHTML = `R$ ${total.toFixed(2)}`;
    valorTotal.innerHTML = `R$ ${total.toFixed(2)}`;
}