const btns = document.querySelectorAll('.right-column__btn');

for (let i = 0; i < btns.length; i++) {

    btns.item(i).addEventListener('mouseover', (e) => {
        e.currentTarget.style.border = "3px solid #99a99a"
    });

    btns.item(i).addEventListener('mouseout', (e) => {
        e.target.style.border = 'none'
    });

    btns.item(i).addEventListener('click', (e) => {
        e.target.style.border = 'none'
    });

}
