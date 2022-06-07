document.querySelector("input#id_username").placeholder = "Введите логин";
document.querySelector("input#id_password").placeholder = "Введите пароль";

const closeBtn = document.querySelector('.form-close');

closeBtn.addEventListener('click', (e) => {
    e.preventDefault();
    history.back();
});
