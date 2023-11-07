// Código JavaScript para interatividade das estrelas
// adicionando um evento de clique a cada estrela
// chamar a função `alert()` com a classificação selecionada

$('.star').click(function () {
    // Obtém a classificação selecionada
    var rating = $(this).data('rating');

    // Exibe um alerta com a classificação selecionada
    alert("Você avaliou com " + rating + " estrelas, obrigado!!!");
});
