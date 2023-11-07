//Declara duas variáveis globais, displayedQuestions e displayedResponses
//Essas variáveis serão usadas para armazenar as perguntas e respostas já exibidas.
var displayedQuestions = [];
var displayedResponses = [];

//função é responsável por obter a resposta do usuário e exibi-la no container de mensagens.
function getUserResponse() {

    // Obter o texto do input do usuário
    var userText = $('#textInput').val();

    // Criar um elemento `div` com a classe `message` e a classe `user-message`
    var userHTML = "<div class='message user-message'><p>User: " + userText + "</p></div>";

    // Limpar o input do usuário
    $('#textInput').val("");

    // Adicionar o elemento `div` ao container de mensagens
    $('.message-container').append(userHTML);

    // Fazer uma solicitação Ajax para o servidor
    $.ajax({
        url: '/auth/chatbot/',
        type: 'POST',
        data: {
            csrfmiddlewaretoken: csrf_token,
            user_input: userText
        },
        success: function (data) {
            if (data && data.text !== undefined) {
                // Obter a resposta do servidor
                var responseText = data.text || '';

                // Verificar se a resposta já foi exibida
                if (!displayedResponses.includes(responseText)) {

                    // Criar um elemento `div` com a classe `message` e a classe `bot-message`
                    var botHTML = "<div class='message bot-message'><p>Chatbot: " + responseText + "</p></div>";

                    // Adicionar o elemento `div` ao container de mensagens
                    $('.message-container').append(botHTML);

                    // Adicionar a resposta à variável global
                    displayedResponses.push(responseText);
                }
            }
        },
        //callback é chamado quando ocorre um erro na solicitação Ajax(é usado somente para fins de testes)
        error: function (xhr, status, error) {
            console.error(xhr.responseText);
        }
    });

    // Verificar se a pergunta já foi exibida
    if (!displayedQuestions.includes(userText)) {

        // Adicionar a pergunta à variável global
        displayedQuestions.push(userText);

        // Criar um elemento `div` com a classe `message` e a classe `bot-message`
        var botHTML = "<div class='message bot-message'><p>Chatbot: " + responseText + "</p></div>";

        // Adicionar o elemento `div` ao container de mensagens
        $('.message-container').append(botHTML);
    }
}

// O código a seguir adiciona um evento de clique ao botão `buttonInput`
// para chamar a função `getUserResponse()`

$('#buttonInput').click(function () {
    getUserResponse();
});

// O código a seguir adiciona um evento de clique ao botão `clearButton`
// para remover todas as mensagens do container de mensagens

$('#clearButton').click(function () {
    $('.user-message, .bot-message').remove(); // Remove todas as mensagens
});



