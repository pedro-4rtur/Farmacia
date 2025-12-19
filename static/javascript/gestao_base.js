// Script simples para Toggle da Sidebar em Mobile
const sidebar = document.getElementById('sidebar');
const toggleBtn = document.getElementById('sidebarToggle');

// Verifica se a tela é pequena para mostrar o botão
function checkResize() {
    if (window.innerWidth <= 992) {
        if(toggleBtn) toggleBtn.style.display = 'block';
    } else {
        if(toggleBtn) toggleBtn.style.display = 'none';
    }
}

window.addEventListener('resize', checkResize);
checkResize(); // Executa ao carregar

if (toggleBtn) {
    toggleBtn.addEventListener('click', () => {
        sidebar.classList.toggle('active');
    });
}