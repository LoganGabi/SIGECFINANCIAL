function updateForm() {
    // Obter o valor selecionado
    var selectedForm = document.getElementById('formSelect').value;
    //  formulários
    var form1 = document.getElementById('form1');
    var form2 = document.getElementById('form2');
    var form3 = document.getElementById('form3');
    // Lista de formulários para iterar
    var forms = [form1, form2, form3];
    // Função auxiliar para configurar cada formulário
    function configureForm(form, isActive) {
        if (isActive) {
            form.style.display = 'block'; // Exibe o formulário
            form.querySelectorAll('input, select, textarea').forEach(function (field) {
                field.removeAttribute('disabled'); // Habilita os campos
                field.setAttribute('required', ''); // Adiciona required
            });
        } else {
            form.style.display = 'none'; // Oculta o formulário
            form.querySelectorAll('input, select, textarea').forEach(function (field) {
                field.setAttribute('disabled', ''); // Desabilita os campos
                field.removeAttribute('required'); // Remove required
            });
        }
    }
    // Configura os formulários com base na seleção
    if (selectedForm === 'Pessoa Fisica') {
        configureForm(form1, true); // Mostra Pessoa Fisica
        configureForm(form2, false); // Oculta Pessoa Juridica
        configureForm(form3, false); // Oculta Estrangeiro
    } else if (selectedForm === 'Pessoa Juridica') {
        configureForm(form1, false); // Oculta Pessoa Fisica
        configureForm(form2, true); // Mostra Pessoa Juridica
        configureForm(form3, false); // Oculta Estrangeiro
    } else if (selectedForm === 'Estrangeiro') {
        configureForm(form1, false); // Oculta Pessoa Fisica
        configureForm(form2, false); // Oculta Pessoa Juridica
        configureForm(form3, true); // Mostra Estrangeiro
    } else {
        // Caso nenhuma opção seja selecionada, oculta todos os formulários
        forms.forEach(form => configureForm(form, false));
    }
}
window.onload = function () {
    updateForm();
};