"use strict"

const wrapper = document.getElementsByClassName('wrapper')[0];


//Работа с формой добавления документов:
//кнопка открытия формы:
const btnAddDoc = document.getElementsByClassName('table__btn-add-doc')[0];
 //формы изменения заявки:
const formAddDoc = document.getElementsByClassName('form-doc add')[0];
//кнопка закрытия формы btnReset
const btnResetDocAdd = document.getElementsByClassName('bnt-form-doc-reset-add')[0];

//Работа с формой добавить заявку:

//кнопка открытия формы:
const btnAddApp = document.getElementsByClassName('table__btn-add-app')[0];
//форма добавления заявки:
const formAddApp = document.getElementsByClassName('form-app add')[0];
//кнопка закрытия формы
const btnResetAppAdd = document.getElementsByClassName('bnt-form-app-reset-add')[0];

// Форма удаления документа:

// Форма подтверждения удаления
const formToConfirmDelete = document.getElementsByClassName('confirm-delete')[0];
// id удаляемого документа
const actionInputDelete = document.getElementById('action-delete');

// Форма сообщения:
const message_box = document.getElementsByClassName('messages')[0];
// Кнопка закрытия сообщения:
const message_close = document.getElementsByClassName('close')[0];


document.addEventListener('click', function (event) {

    const evenClassName = event.target.className;
    // Открытие/Закрытие формы добавления заявки:
    if (evenClassName === btnAddApp.className || btnResetAppAdd.contains(event.target)) {
        formAddApp.classList.toggle('data-show-or-hide-form');
        wrapper.classList.toggle('blackout');
    }
    // Открытие/Закрытие формы добавления документа:
    else if (evenClassName === btnAddDoc.className || btnResetDocAdd.contains(event.target)) {
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

    // Закрытие сообщения
    if (evenClassName === message_close.className){
        message_box.style.display = "none"
    }
});

//ErrorList
const errorList = document.querySelector(".form-app__timing > ul.errorlist")
if (errorList.length !== 0) {
    formAddDoc.classList.add('data-show-or-hide-form');
    wrapper.classList.add('blackout');
}