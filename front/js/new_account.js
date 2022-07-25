"use strict"

//формы добавление документа:
const formAddDoc = document.getElementsByClassName('form-doc add')[0];
const wrapper = document.getElementsByClassName('wrapper')[0];

document.addEventListener('click', function (event) {

    const evenClassName = event.target.className;

    //кнопка открытия формы (добавления документа):
    const btnAddDoc = this.getElementsByClassName('table__btn-add-doc')[0];
    //кнопка закрытия формы (добавления документа):
    const btnResetDocAdd = document.getElementsByClassName('bnt-form-doc-reset-add')[0];
    // Форма подтверждения удаления (документа)
    const formToConfirmDelete = this.getElementsByClassName('confirm-delete')[0];
    // Кнопка отмены удаления (документа)
    const actionInputDelete = this.getElementById('action-delete');

     // Форма сообщения:
    const message_box = this.getElementsByClassName('messages')[0];
    // Кнопка закрытия сообщения:
    const message_close = this.getElementsByClassName('close')[0];


     if (evenClassName === btnAddDoc.className || btnResetDocAdd.contains(event.target)) {
         formAddDoc.classList.toggle('data-show-or-hide-form');
         wrapper.classList.toggle('blackout');
     }

    if (evenClassName === 'table__btn-delete-app') {
        actionInputDelete.value = event.target.id;
        formToConfirmDelete.classList.toggle('data-show-or-hide-form');
        wrapper.classList.toggle('blackout');

    } else if (event.target.id === 'btn-refuse-delete') {
        formToConfirmDelete.classList.toggle('data-show-or-hide-form');
        wrapper.classList.toggle('blackout');
    }
    if (evenClassName === message_close.className){
        message_box.style.display = "none"
    }

});

//ErrorList
const errorList = document.querySelector(".form-app__timing > span > ul.errorlist")

if (errorList.length !== 0) {
    formAddDoc.classList.add('data-show-or-hide-form');
    wrapper.classList.add('blackout');
}