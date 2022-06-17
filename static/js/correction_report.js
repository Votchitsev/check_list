const hasGivenDiv = document.querySelectorAll('.correction_report_providing_checking_container__item')[0];
const hasCompletedDiv = document.querySelectorAll('.correction_report_providing_checking_container__item')[1];
const form = document.forms[0];
const commentText = form.querySelector('textarea');
const deleteBtns = document.querySelectorAll('.correction_report_comments__item__delete')


if (hasGivenDiv.textContent == 'Не представлен') {
    hasGivenDiv.classList.add('negative');
    hasGivenDiv.classList.remove('positive');
} else {
    hasGivenDiv.classList.add('positive');
    hasGivenDiv.classList.remove('negative');
}

if (hasCompletedDiv.textContent == 'Не отработан') {
    hasCompletedDiv.classList.add('negative');
    hasCompletedDiv.classList.remove('positive');
} else {
    hasCompletedDiv.classList.add('positive');
    hasCompletedDiv.classList.remove('negative');
}
