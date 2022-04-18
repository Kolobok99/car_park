"use strict"

document.addEventListener('click', function (event) {

    const evenClassName = event.target.className;
    const wrapper = document.getElementsByClassName('wrapper')[0];
    
    //Работа с формой добавить:

    //кнопка открытия формы:
    const btnAddApp = this.getElementsByClassName('table__btn-add-app')[0];
    //форма добавления заявки:
    const formAdd = document.getElementsByClassName('form-app add')[0];
    //кнопка закрытия формы
    const btnResetAppAdd = document.getElementsByClassName('bnt-form-app-reset-add')[0];

    //Работа с формой добавления документов:
    
    //кнопка открытия формы:
    const btnAddDoc = this.getElementsByClassName('table__btn-add-doc')[0];

     //формы изменения заявки:
    const formAddDoc = this.getElementsByClassName('form-doc add')[0];
    
    //кнопка закрытия формы btnReset
    const btnResetDocAdd = document.getElementsByClassName('bnt-form-doc-reset-add')[0];

    if (evenClassName == btnAddApp.className || btnResetAppAdd.contains(event.target)) {
        formAdd.classList.toggle('data-show-or-hide-form');
        wrapper.classList.toggle('blackout');
    // } else if (evenClassName == btnChangeApp.className || btnResetAppChange.contains(event.target)) {
    //     formChange.classList.toggle('data-show-or-hide-form');
    //     wrapper.classList.toggle('blackout');
    } else if (evenClassName == btnAddDoc.className || btnResetDocAdd.contains(event.target)) {
        formAddDoc.classList.toggle('data-show-or-hide-form');
        wrapper.classList.toggle('blackout');
    };


    // Форма удаления документа:

    const buttonToDeleteDoc = this.getElementsByClassName('table__btn-delete-app');
    const formToConfirmDelete = this.getElementsByClassName('confirm-delete')[0];
    const buttonConfirmDelete = this.getElementById('btn-confirm-delete')[0];
    const buttonRefuseDelete = this.getElementById('btn-refuse-delete');
    const actionInputDelete = this.getElementById('action-delete');

    // При нажатии на кнопку удаления документа
    // Получить ее id
    // добавить этот id в value скрытого поля формы подтверждения
    // wrapper blackout и форма подтверждения show

    if (evenClassName == 'table__btn-delete-app') {
        const buttonDeleteId = event.target.id;
        console.log(buttonDeleteId);
        actionInputDelete.value = buttonDeleteId;
        // console.log(actionInputDelete.value);
        formToConfirmDelete.classList.toggle('data-show-or-hide-form');
        wrapper.classList.toggle('blackout');
        console.log('123');

    } else if (event.target.id == 'btn-refuse-delete') {
        console.log('456');
        formToConfirmDelete.classList.toggle('data-show-or-hide-form');
        wrapper.classList.toggle('blackout');
    }
    
    console.log(evenClassName);
    // if (evenClassName == btnChangeApp.className) {
    //     const eventTargetId = event.target.id;
    //     const eventTargetOnlyId = eventTargetId.replace(/[^\d]/g, '')
    //     const titleAppId = this.getElementById('data-title-app-id');
        
    //     titleAppId.textContent = parseInt(eventTargetOnlyId);
        
    //     // const appChangeHidden = this.getElementById(`app-change-hidden-${eventTargetOnlyId}`);
    //     // appChangeHidden.value = "";
    // }

});