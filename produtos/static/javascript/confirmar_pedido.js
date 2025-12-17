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

function finalizarPedido() {
    const btn = document.querySelector('.btn-confirm');
    btn.innerHTML = '<i class="bi bi-spin"></i> PROCESSANDO...';
    btn.style.opacity = '0.8';

    const csrftoken = getCookie('csrftoken');
    const url = "/pedidos/criar-pedido";

    // Faz a requisição para o backend
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.sucesso) {
            // Abre o modal após "sucesso"
            openModal();
            
            // Restaura botão (opcional)
            btn.innerHTML = "Pedido finalizado";
            btn.disabled = true;

            // 2. Atualiza o ícone do carrinho no cabeçalho (se houver um contador)
            const contador = document.getElementById('contagem-cesta');
            if (contador) {
                contador.innerText = 0;
            }
        } else {
            alert('Erro ao confirmar a compra: ' + data.erro);
            window.location.href = '/pedidos/confirmar-pedido';
        }
    })
    .catch(error => console.error('Erro:', error));
}

const modal = document.getElementById('orderConfirmationModal');

// Função para ABRIR o modal
// Chame esta função dentro da sua função "finalizarPedido()" existente
function openModal() {
    modal.classList.add('active');
}

// Função para FECHAR o modal
function closeModal() {
    modal.classList.remove('active');
}