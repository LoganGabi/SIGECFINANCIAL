document.addEventListener("DOMContentLoaded", function () {
    var selectedForm = document.body.getAttribute('data-selected-form');
    var form1 = document.getElementById('form1');
    var form2 = document.getElementById('form2');
    var form3 = document.getElementById('form3');

    function configureForm(form, isActive) {
        if (isActive) {
            form.style.display = 'block';
            form.querySelectorAll('input, select, textarea').forEach(function (field) {
                field.removeAttribute('disabled');
                field.setAttribute('required', '');
            });
        } else {
            form.style.display = 'none';
            form.querySelectorAll('input, select, textarea').forEach(function (field) {
                field.setAttribute('disabled', '');
                field.removeAttribute('required');
            });
        }
    }

    if (selectedForm === 'Pessoa Fisica') {
        configureForm(form1, true);
        configureForm(form2, false);
        configureForm(form3, false);
    } else if (selectedForm === 'Pessoa Juridica') {
        configureForm(form1, false);
        configureForm(form2, true);
        configureForm(form3, false);
    } else if (selectedForm === 'Estrangeiro') {
        configureForm(form1, false);
        configureForm(form2, false);
        configureForm(form3, true);
    } else {
        configureForm(form1, false);
        configureForm(form2, false);
        configureForm(form3, false);
    }
});