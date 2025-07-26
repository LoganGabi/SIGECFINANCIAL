// Seleciona o botão de toggle e a sidebar
const toggleButton = document.querySelector('.toggle-menu');
const sidebar = document.querySelector('.sidebar');
const content = document.querySelector('.content'); // Adicionado para referenciar o conteúdo
const toggles = document.querySelectorAll('.toggle');
// Alterna a visibilidade da sidebar
toggleButton.addEventListener('click', () => {
    sidebar.classList.toggle('hidden');
    content.classList.toggle('expanded'); // Alterna a classe no conteúdo
});
 const notificationContainer = document.getElementById("notificationContainer");
const buttonNotification = document.getElementById("buttonNotification");
// Seleciona o botão e o menu
const userMenuButton = document.getElementById('user-menu-button');
const userDropdownMenu = document.getElementById('user-dropdown-menu');

// Adiciona um evento de clique para mostrar/ocultar o menu
userMenuButton.addEventListener('click', function(event) {
    // Impede que o clique no botão feche o menu imediatamente
    event.stopPropagation();
    
    // Alterna a visibilidade do menu
    const isMenuVisible = userDropdownMenu.style.display === 'block';
    userDropdownMenu.style.display = isMenuVisible ? 'none' : 'block';
    notificationContainer.style.display = "none";
});

// Fecha o menu se o usuário clicar fora dele
window.addEventListener('click', function(event) {
    if (!userDropdownMenu.contains(event.target) && event.target !== userMenuButton) {
        userDropdownMenu.style.display = 'none';
    }
    if(!notificationContainer.contains(event.target) && event.target !== buttonNotification){
        notificationContainer.style.display = "none";
    }
    
});

document.addEventListener("DOMContentLoaded", function () {
    const toggles = document.querySelectorAll(".toggle");
    let notificationExists = false;
    toggles.forEach((toggle, index) => {
        const submenu = toggle.nextElementSibling; // Pegamos o submenu associado

        //Recupera o estado salvo no localStorage
        const estadoSalvo = localStorage.getItem(`submenu-${index}`);

  
        if (estadoSalvo === "block") {
            submenu.style.display = "block";
            toggle.classList.replace( "toggle","rotate")
        } else {
            submenu.style.display = "none";
            
            toggle.classList.replace("rotate", "toggle");
        }

        toggle.addEventListener("click", function () {
            const displayAtual = window.getComputedStyle(submenu).display;

            if (displayAtual === "none") {
                submenu.style.display = "block";
                localStorage.setItem(`submenu-${index}`, "block"); // Salva o estado
                toggle.classList.replace( "toggle","rotate")
            } else {
                submenu.style.display = "none";
                localStorage.setItem(`submenu-${index}`, "none"); // Salva o estado
                toggle.classList.replace("rotate", "toggle");
            }
        });
    });

    fetch(`/notifications/`) .then(response => {
        if (response.ok && response.headers.get('Content-Type').includes('application/json')) {
            return response.json();
        } else {
            throw new Error('Response is not JSON');
        }
    })
    .then(data=>{
        const notificationBadge = document.getElementById("notification-badge");
        const notificationContainer = document.getElementById("notificationContainer");
        if(data.notifications.length >= 1){
            notificationBadge.style.display = "block";
            notificationExists = true;
        }
        data.notifications.forEach(notification=>{
            const newNotification = document.createElement("div");
            const dateFormated = new Date(notification.date).toLocaleDateString('pt-BR');
            newNotification.innerHTML = `${dateFormated}: Pagamento ${notification.idPayment} precisa ser pago em ${notification.remainsDays} dias!`
            newNotification.classList.add("notification");
            notificationContainer.appendChild(newNotification);
        })
    })

    const buttonNotification = document.getElementById("buttonNotification");
    buttonNotification.addEventListener("click",(event)=>{
        event.stopPropagation();

        const isMenuVisible = notificationContainer.style.display === "block";

        notificationContainer.style.display = isMenuVisible ? 'none' : 'block';
        userDropdownMenu.style.display = 'none';
    })
    
});
