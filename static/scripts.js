document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("cadastroForm");
    const nome = document.getElementById("nome");
    const email = document.getElementById("email");
    const senha = document.getElementById("senha");

    const erroNome = document.getElementById("erroNome");
    const erroEmail = document.getElementById("erroEmail");
    const erroSenha = document.getElementById("erroSenha");
    const mensagemServidor = document.getElementById("mensagemServidor");

    form.addEventListener("submit", async function (e) {
        e.preventDefault();

        erroNome.textContent = "";
        erroEmail.textContent = "";
        erroSenha.textContent = "";
        mensagemServidor.innerHTML = "";

        let valido = true;

        if (nome.value.trim().length < 3) {
            erroNome.textContent = "O nome deve ter pelo menos 3 caracteres.";
            valido = false;
        }

        const regexEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!regexEmail.test(email.value.trim())) {
            erroEmail.textContent = "E-mail inválido.";
            valido = false;
        }

        const regexSenha = /^(?=.*[A-Z])(?=.*\d).{8,}$/;
        if (!regexSenha.test(senha.value)) {
            erroSenha.textContent = "A senha deve ter pelo menos 8 caracteres, incluindo uma letra maiúscula e um número.";
            valido = false;
        }

        if (!valido) return;

        const formData = new FormData(form);

        try {
            const resposta = await fetch("/enviar", {
                method: "POST",
                body: formData
            });

            const texto = await resposta.text();

            if (resposta.ok) {
                mensagemServidor.style.color = "green";
                form.reset(); // limpa o formulário em caso de sucesso
            } else {
                mensagemServidor.style.color = "red";
            }

            mensagemServidor.innerHTML = texto;

        } catch (err) {
            mensagemServidor.style.color = "red";
            mensagemServidor.textContent = "Erro ao conectar com o servidor.";
        }
    });
});
