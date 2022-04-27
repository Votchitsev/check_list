
const mainReportFormSubmit = document.querySelector('.main-report-form > #submit');

window.onload = () => {
    const element = mainReportFormSubmit.parentElement.querySelectorAll('#start_date, #finish_date');
    element[0].value = '';
    element[1].value = '';
}
