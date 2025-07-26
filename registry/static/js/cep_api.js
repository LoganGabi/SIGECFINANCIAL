

function limpa_formulário_cep() {
    // Limpa valores do formulário de CEP.
    document.getElementById('id_road').value = "";
    document.getElementById('id_neighborhood').value = "";
    document.getElementById('id_complement').value = "";
    document.getElementById('id_city').value = "";
    document.getElementById('id_uf').value = "";
}

function meu_callback(conteudo) {
    if (!("erro" in conteudo)) {
        // Atualiza os campos com os valores.
        document.getElementById('id_road').value = conteudo.logradouro || "";
        document.getElementById('id_neighborhood').value = conteudo.bairro || "";
        document.getElementById('id_complement').value = conteudo.complemento || "";
        document.getElementById('id_city').value = conteudo.localidade || "";
        document.getElementById('id_uf').value = conteudo.uf || "";
    } else {
        // CEP não encontrado.
        limpa_formulário_cep();
        alert("CEP não encontrado.");
    }
}

function pesquisacep(valor) {
    // Nova variável "cep" somente com dígitos.
    var cep = valor.replace(/\D/g, '');

    // Verifica se o campo cep possui valor informado.
    if (cep !== "") {
        // Expressão regular para validar o CEP.
        var validacep = /^[0-9]{8}$/;

        // Valida o formato do CEP.
        if (validacep.test(cep)) {
            // Preenche os campos com "..." enquanto consulta o webservice.
            document.getElementById('id_road').value = "...";
            document.getElementById('id_neighborhood').value = "...";
            document.getElementById('id_complement').value = "...";
            document.getElementById('id_city').value = "...";
            document.getElementById('id_uf').value = "...";

            // Cria um elemento JavaScript para a requisição.
            var script = document.createElement('script');
            // Sincroniza com o callback.
            script.src = 'https://viacep.com.br/ws/' + cep + '/json/?callback=meu_callback';
            // Insere script no documento e carrega o conteúdo.
            document.body.appendChild(script);
        } else {
            // CEP é inválido.
            limpa_formulário_cep();
            alert("Formato de CEP inválido.");
        }
    } else {
        // CEP sem valor, limpa formulário.
        limpa_formulário_cep();
    }
}