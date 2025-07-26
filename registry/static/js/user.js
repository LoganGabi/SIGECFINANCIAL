
function mostrarCampos() {
    const check_user = document.getElementById('id_isUser');
    const campos = document.getElementById('campos');

    if (check_user.checked) {
      campos.style.display = 'inline';
    } else {
      campos.style.display = 'none';
    }
  }

  
function mostrarSenha() {
    const input = document.getElementById('id_password');
    const icone = document.getElementById('icone-olho');

    if (input.type === 'password') {
    input.type = 'text';
    icone.classList.remove('bi-eye');
    icone.classList.add('bi-eye-slash');
    } else {
    input.type = 'password';
    icone.classList.remove('bi-eye-slash');
    icone.classList.add('bi-eye');
    }
}

// AVISO: VAI CAUSAR PROBLEMAS NA PAGINA,
// SE HOUVER OUTRO SCRIPT COM A FUNCAO Window.onload
// window.onload = function () {
//     // mostrarCampos();
// };