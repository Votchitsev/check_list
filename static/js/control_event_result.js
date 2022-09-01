const btns = document.querySelectorAll('.right-column__btn');
const gradeElements = document.querySelectorAll('.check_list__position__grade');

for (let i = 0; i < btns.length; i++) {

    btns.item(i).addEventListener('mouseenter', (e) => {
        e.currentTarget.style.border = "3px solid #99a99a"
    });

    btns.item(i).addEventListener('mouseleave', (e) => {
        e.target.style.border = 'none'
    });

    btns.item(i).addEventListener('click', (e) => {
        e.target.style.border = 'none'
    });

}

for (let i = 0; i < gradeElements.length; i++) {

    let element = gradeElements.item(i);

    if (element.textContent == 'Да') {
        element.style.backgroundColor = "#749b74";
    }

    if (element.textContent == "Нет") {
        element.style.backgroundColor = '#f37171';
    }
}
