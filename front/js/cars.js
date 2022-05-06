"use strict"

//wrapper
const wrapper = document.getElementsByClassName('wrapper')[0];
//формы изменения заявки:
const formAddDoc = document.getElementsByClassName('form-car add')[0];
document.addEventListener('click', function (event) {

    const evenClassName = event.target.className;
    //Работа с формой добавления документов:

    //кнопка открытия формы:
    const btnAddDoc = this.getElementsByClassName('main__btn-add-car')[0];

    //кнопка закрытия формы btnReset
    const btnResetDocAdd = document.getElementsByClassName('bnt-form-car-reset-add')[0];

    if (evenClassName == btnAddDoc.className || btnResetDocAdd.contains(event.target)) {
        formAddDoc.classList.toggle('data-show-or-hide-form');
        wrapper.classList.toggle('blackout');
    }

    const message_box = this.getElementsByClassName('messages')[0];
    // Кнопка закрытия сообщения:
    const message_close = this.getElementsByClassName('close')[0];

      if (evenClassName == message_close.className){
        console.log('YES!')
        message_box.style.display = "none"
    }
    //
    // if (evenClassName == 'table__btn-add-app') {
    //     formAdd.classList.toggle('data-show-or-hide-form');
    //     wrapper.classList.toggle('overlay');
    // } else if (btnReset.contains(event.target)) {
    //     console.log('YES!');
    //     formAdd.classList.toggle('data-form-add');
    //     wrapper.classList.toggle('overlay');
    // } else if (evenClassName == 'table__btn-change-app') {
    //
    // }
});

const errorList = document.getElementsByClassName("errorlist");
console.log(errorList.length);
if (errorList.length != 0) {
    console.log('YES!');
    formAddDoc.classList.add('data-show-or-hide-form');
    wrapper.classList.add('blackout');
}