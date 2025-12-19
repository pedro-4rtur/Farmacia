document.addEventListener('DOMContentLoaded', () => {
  // Elementos
  const modal = document.querySelector('.modal-overlay');
  const closeModalBtn = document.querySelector('.close-modal');
  const cancelBtn = document.getElementById('btnCancel');
  const applyBtn = document.getElementById('btnApply');
  
  // O ID que está no seu HTML é "filter-btn" (no <th>)
  const filterTrigger = document.getElementById('filter-btn');
  
  // Função para abrir modal
  function openModal() {
    if (modal) {
        // Usa FLEX para respeitar a centralização do CSS
        modal.style.display = 'flex'; 

    }
  }

  // Função para fechar modal
  function closeModal() {
    if (modal) {
        modal.style.display = 'none';
    }
  }

  // Event Listeners
  if (filterTrigger) {
      filterTrigger.addEventListener('click', (e) => {
          e.preventDefault(); // Previne comportamentos estranhos
          openModal();
      });
      // Adiciona estilo de cursor para indicar que é clicável
      filterTrigger.style.cursor = 'pointer';
  } else {
      console.error('Botão de filtro (#filter-btn) não encontrado!');
  }
  
  // Fechar no X ou no Cancelar
  if (closeModalBtn) closeModalBtn.addEventListener('click', closeModal);
  if (cancelBtn) cancelBtn.addEventListener('click', closeModal);

  // Fechar se clicar fora do modal
  window.addEventListener('click', (e) => {
    if (e.target === modal) {
      closeModal();
    }
  });

  // Ação de Aplicar Filtro
  if (applyBtn) {
      applyBtn.addEventListener('click', () => {
        const checkboxes = document.querySelectorAll('input[name="status"]:checked');
        let selectedStatuses = Array.from(checkboxes).map(cb => cb.value);
    
        const rows = document.querySelectorAll('tbody tr');
    
        rows.forEach(row => {
            const statusRow = row.getAttribute('data-status'); // Agora vai funcionar
            
            // Atenção: O status no banco é 'P', 'E', 'C'? 
            // Se for, você precisará converter 'pendente' para 'P' aqui ou no HTML.
            // Exemplo de verificação simples:
            if (selectedStatuses.length === 0 || (statusRow && selectedStatuses.some(s => s.charAt(0).toUpperCase() === statusRow))) {
                row.style.display = ''; 
            } else {
                row.style.display = 'none';
            }
        });
        
        closeModal();
      });
  }
});