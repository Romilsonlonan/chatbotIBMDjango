// Código JavaScript para interatividade das estrelas
// adicionando um evento de clique a cada estrela
// enviando a classificação para o back-end
// exibindo um alerta com efeito de pisca-pisca

$(function() {
    $('.rating .star').click(function() {
      var rating = $(this).data('rating');

      // Envie a classificação para o back-end
      $.ajax({
        url: '/feedback',
        data: {
            rating: rating
        },
        type: 'POST'
      });

      // Exibe um alerta com efeito de pisca-pisca
      var alert = document.createElement('div');
      alert.textContent = 'Obrigado pelo feedback! Sua classificação foi de {}.'.format(rating);
      alert.style.color = 'green';
      alert.style.backgroundColor = 'white';
      alert.style.animation = 'blink 1s 0.5s infinite';

      document.body.appendChild(alert);
    });
  });

