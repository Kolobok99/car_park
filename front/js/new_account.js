"use strict"

document.addEventListener('click', function (event) {

    const evenClassName = event.target.className;
    const wrapper = document.getElementsByClassName('wrapper')[0];

    //Работа с формой добавления документов:
    //кнопка открытия формы:
    const btnAddDoc = this.getElementsByClassName('table__btn-add-doc')[0];
     //формы изменения заявки:
    const formAddDoc = this.getElementsByClassName('form-doc add')[0];
    //кнопка закрытия формы btnReset
    const btnResetDocAdd = document.getElementsByClassName('bnt-form-doc-reset-add')[0];

    // Форма подтверждения удаления
    const formToConfirmDelete = this.getElementsByClassName('confirm-delete')[0];
    // Кнопка отмены удаления
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