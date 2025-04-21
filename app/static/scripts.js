$(document).ready(function() {
    $('#formCadastro').submit(function(event) {
        event.preventDefault();

        var nome = $('#nome').val();
        var email = $('#email').val();
        var senha = $('#senha').val();

        $.ajax({
            url: '/cadastro',
            type: 'POST',
            data: {
                nome: nome,
                email: email,
                senha: senha
            },
            success: function(response) {
                $('#mensagemCadastro').text(response);
            },
            error: function(xhr) {
                var errorMessage = xhr.responseText || 'Erro ao cadastrar.';
                $('#mensagemCadastro').text(errorMessage);
            }
        });
    });

    $('#formLogin').submit(function(event) {
        event.preventDefault();

        var loginEmail = $('#loginEmail').val();
        var loginSenha = $('#loginSenha').val();

        $.ajax({
            url: '/login',
            type: 'POST',
            data: {
                email: loginEmail,
                senha: loginSenha
            },
            success: function(response) {
                $('#mensagemLogin').text(response);
            },
            error: function(xhr) {
                var errorMessage = xhr.responseText || 'Erro ao fazer login.';
                $('#mensagemLogin').text(errorMessage);
            }
        });
    });
});
