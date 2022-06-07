const closeBtn = document.querySelector('.form-close');

closeBtn.addEventListener('click', (e) => {
    e.preventDefault();
    history.back();
});