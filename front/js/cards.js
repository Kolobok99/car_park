"use strict"
//wrapper
const wrapper = document.getElementsByClassName('wrapper')[0];
//формы изменения заявки:
const formAddDoc = document.getElementsByClassName('form-card add')[0];

document.addEventListener('click', function (event) {

    const evenClassName = event.target.className;

    //Работа с формой добавления документов:
    
    //кнопка открытия формы:
    const btnAddDoc = this.getElementsByClassName('main__btn-add-card')[0];
    //кнопка закрытия формы btnReset
    const btnResetDocAdd = document.getElementsByClassName('bnt-form-card-reset-add')[0];

    if (evenClassName == btnAddDoc.className || btnResetDocAdd.contains(event.target)) {
        formAddDoc.classList.toggle('data-show-or-hide-form');
        wrapper.classList.toggle('blackout');
    };
});

const errorList = document.getElementsByClassName("errorlist");

console.log(errorList.length);
if (errorList.length != 0) {
        console.log('YES!');
        formAddDoc.classList.add('data-show-or-hide-form');
        wrapper.classList.add('blackout');
    }


