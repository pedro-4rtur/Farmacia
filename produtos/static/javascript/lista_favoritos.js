// 1. Selecionar os elementos
const container = document.querySelector('.container-produtos'); // A div com overflow: hidden
const btnPrev = document.querySelector('.prev-button');
const btnNext = document.querySelector('.next-button');

// 2. Definir a função de rolagem
function rolarCarrossel(direcao) {
    const scrollAmount = 200;

    if (direcao === 'next') {
        container.scrollBy({
            left: scrollAmount, // Valor positivo rola para a direita
            behavior: 'smooth'  // Faz a animação suave
        });
    } else {
        container.scrollBy({
            left: -scrollAmount, // Valor negativo rola para a esquerda
            behavior: 'smooth'
        });
    }
}

// 3. Adicionar os eventos de clique
btnNext.addEventListener('click', () => rolarCarrossel('next'));
btnPrev.addEventListener('click', () => rolarCarrossel('prev'));