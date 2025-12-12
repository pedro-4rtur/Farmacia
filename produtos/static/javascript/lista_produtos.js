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

document.querySelector(".container-produtos").addEventListener("click", function(e) {
    const btnFavorito = e.target.closest(".favorite-btn");
    let icone = btnFavorito.querySelector("i");
    let operacao = icone.classList.contains("bi-heart-fill") ? "remover" : "adicionar";
    const url = "/favorito/"+operacao;

    e.preventDefault();
    e.stopPropagation();

    const produtoId = btnFavorito.dataset.produtoId;
    const csrftoken = getCookie('csrftoken');

    fetch(url, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'produto_id': produtoId})
    })
    .then(response => response.json())
    .then(data => {
        if (data.sucesso) {
            let contagemFavorito = document.querySelector("#contagem-favorito")

            if(icone.classList.contains("bi-heart-fill")) {
                icone.classList.add("bi-heart");
                icone.classList.remove("bi-heart-fill");
            } else {
                icone.classList.add("bi-heart-fill");
                icone.classList.remove("bi-heart");
            }
            

            contagemFavorito.innerHTML = data.contagemFavoritos
        } else {
            alert('Erro ao adicionar: ' + data.erro);
            window.location.href = "/login";
        }
    })
    .catch(error => console.error('Erro:', error));
})