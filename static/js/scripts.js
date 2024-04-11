console.log("loading js/scripts");

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


$(document).ready(function() {

    // Altera a quantidade de Potes no carrinho.
    $(document).on('click', '.sacola_plus, .sacola_minus', function(){
        // Obtem o Identificador do Pote
        // closest procra o ancestral mais próximo subindo na hierarquia do DOM a partir do elemento atual
        var poteId = $(this).closest('.pote-item').data('poteid');

        // Use .siblings() para encontrar o elemento irmão do botão clicado
        var inputCountPote = $(this).siblings('input.countCartItem_'+poteId); 
        
        // Atualiza a quantidade no frontend
        if ($(this).hasClass('sacola_plus')) {
            // Incrementa a quantidade quando o botão de adição é clicado
            inputCountPote.val(parseInt(inputCountPote.val()) + 1); 
        } else if ($(this).hasClass('sacola_minus')) {
            // Decrementa a quantidade, com um valor mínimo de 0, quando o botão de subtração é clicado
            inputCountPote.val(Math.max(parseInt(inputCountPote.val()) - 1, 1));
        }

        var currentValue = parseInt(inputCountPote.val());

        // Exibe a quantidade atual no console
        console.log("Quantidade Atual:", currentValue);

        // Obtenha o token CSRF do cookie
        var csrftoken = getCookie('csrftoken');

        $.ajax({
            url: "/atualiza_quantidade_sacola/",
            type: "POST",
            data: { 
                "poteId" : poteId,
                "novaQuantidade": currentValue,
            }, 
            beforeSend: function (xhr) {
                // Inclua o token CSRF no cabeçalho da requisição
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function (response) {
                console.log(response); 
                var atualizaValor = $('#atualizaValor'); // Substitua 'spanQuantidade_' pelo identificador real que você está usando

                atualizaValor.text(response['novo_valor']);
                
                console.log(response['message'])
                
                $('#messageAlert').text(
                    response['message']).fadeIn(400).delay(2000).fadeOut(400);

            },
            error: function (error) {
                console.error("Erro:", error);
                // Adicione aqui qualquer manipulação adicional em caso de erro.
            }
        }); 
    });  


    // Remover Item da Sacola
    $(document).on('click', '.remove-item', function(){
        // Obtem o Identificador do Pote
        // closest procra o ancestral mais próximo subindo na hierarquia do DOM a partir do elemento atual
        var poteId = $(this).closest('.pote-item').data('poteid');

        console.log("Identificador do Item:", poteId);
 
        // Armazene uma referência ao elemento <li> correspondente
        var poteItem = $(this).closest('.pote-item');

        // Obtenha o token CSRF do cookie
        var csrftoken = getCookie('csrftoken');

        // Envio Ajax com o token CSRF para view atualiza quantidade
        $.ajax({
            url: "/remove_item_sacola/",
            type: "POST",
            data: { "poteId" : poteId },
            beforeSend: function (xhr) {
                // Inclua o token CSRF no cabeçalho da requisição
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function (response) {
                console.log("Sucesso:", response);  
                
                poteItem.fadeOut(400, function() {
                    $(this).remove();
                }); 
                
                var atualizaValor = $('#atualizaValor'); 

                atualizaValor.text(response['novo_valor']);
                console.log(response['message'])
                $('#messageAlert').text(
                    response['message']).fadeIn(400).delay(2000).fadeOut(400);

            },
            error: function (error) {
                console.error("Erro:", error);
                // Adicione aqui qualquer manipulação adicional em caso de erro.
            }
        });
    });


})