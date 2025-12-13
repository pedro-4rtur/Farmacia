// Elementos do DOM
const openBtn = document.getElementById('openMenuBtn');
const closeBtn = document.getElementById('closeMenuBtn');
const overlay = document.getElementById('overlay');
const sideMenu = document.getElementById('sideMenu');

// Funções de abrir e fechar
function openMenu() {
    sideMenu.classList.add('active');
    overlay.classList.add('active');
    document.body.style.overflow = 'hidden'; // Evita scroll na página de fundo
}

function closeMenu() {
    sideMenu.classList.remove('active');
    overlay.classList.remove('active');
    document.body.style.overflow = 'auto'; // Devolve o scroll
}

// Event Listeners
openBtn.addEventListener('click', openMenu);
closeBtn.addEventListener('click', closeMenu);
overlay.addEventListener('click', closeMenu); // Fecha ao clicar fora

// Fechar com a tecla ESC
document.addEventListener('keydown', function(event) {
    if (event.key === "Escape") {
        closeMenu();
    }
});