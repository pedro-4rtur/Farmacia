document.addEventListener('DOMContentLoaded', function() {
            
    // 1. Seleciona todos os links da sidebar
    const links = document.querySelectorAll('.menu-link');
    
    // 2. Seleciona todas as seções de conteúdo
    const contents = document.querySelectorAll('.tab-pane');

    // 3. Adiciona o evento de clique em CADA link
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            // IMPEDE O PULO DE TELA / RECARREGAMENTO
            e.preventDefault();

            // A. Remove a classe 'active' de todos os links e conteúdos
            links.forEach(l => l.classList.remove('active'));
            contents.forEach(c => c.classList.remove('active'));

            // B. Adiciona 'active' apenas no link clicado
            this.classList.add('active');

            // C. Pega o ID alvo (ex: "#enderecos") do atributo href
            const targetId = this.dataset.target; 
            
            // D. Seleciona a div que tem esse ID
            const targetSection = document.querySelector(`#${targetId}`);
            
            // E. Se a seção existir, adiciona 'active' nela para mostrar
            if (targetSection) {
                targetSection.classList.add('active');
            } else {
                console.error('ERRO: Nenhuma seção encontrada com o ID: ' + targetId);
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    
    // ... (seu código existente das abas/sidebar) ...

    // --- LÓGICA DAS MENSAGENS TEMPORÁRIAS ---
    const alerts = document.querySelectorAll('.alert');

    alerts.forEach(alert => {
        // Tempo para começar a sumir (4000ms = 4 segundos)
        setTimeout(() => {
            alert.classList.add('hide'); // Adiciona classe que faz ficar transparente (CSS)
            
            // Espera a transição do CSS terminar (0.5s) para remover do HTML
            setTimeout(() => {
                alert.remove();
            }, 500); 
        }, 4000);
    });
});