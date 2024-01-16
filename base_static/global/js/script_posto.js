// Função para lidar com o comportamento do menu
document.addEventListener('click', function(event) {
    const isMenuOpen = document.body.classList.contains('menu-open');
    const isInsideMenu = document.querySelector('.menu').contains(event.target);
    const isMenuToggle = document.querySelector('.menu-toggle').contains(event.target);
    if (isMenuOpen && !isInsideMenu && !isMenuToggle) {
        document.body.classList.remove('menu-open');
    }
  });
  
  document.querySelector('.menu-toggle').addEventListener('click', function() {
    document.body.classList.toggle('menu-open');
  });
  
  // Função para lidar com a navegação dos sub-tópicos
  $(document).ready(function() {
    var currentSubtopico = $('.subtopico:first').show();  
  
    $('#next').click(function() {
        if (currentSubtopico.next('.subtopico').length) {
            currentSubtopico.hide();
            currentSubtopico = currentSubtopico.next('.subtopico');
            currentSubtopico.show();
        }
        checkButtons();
    });
    
    $('#prev').click(function() {
        if (currentSubtopico.prev('.subtopico').length) {
            currentSubtopico.hide();
            currentSubtopico = currentSubtopico.prev('.subtopico');
            currentSubtopico.show();
        }
        checkButtons();
    });
  
    function checkButtons() {
        $('#prev').prop('disabled', !currentSubtopico.prev('.subtopico').length);
  
        if (currentSubtopico.next('.subtopico').length) {
            $('#next').show();
            $('#save').hide();
        } else {
            $('#next').hide();
            $('#save').show();
        }
    }
  
    checkButtons();
  });
  