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


    //Работа с формой редактирования
    
    // //кнопка открытия формы:
    // const btnChangeApp = this.getElementsByClassName('table__btn-change-app')[0];
    // console.log(btnChangeApp);
    // //формы изменения заявки:
    // const formChange = this.getElementsByClassName('form-app change')[0];

    // //кнопка закрытия формы btnReset
    // const btnResetAppChange = document.getElementsByClassName('bnt-form-app-reset-change')[0];


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
    
    // if (evenClassName == btnChangeApp.className) {
    //     const eventTargetId = event.target.id;
    //     const eventTargetOnlyId = eventTargetId.replace(/[^\d]/g, '')
    //     const titleAppId = this.getElementById('data-title-app-id');
        
    //     titleAppId.textContent = parseInt(eventTargetOnlyId);
        
    //     // const appChangeHidden = this.getElementById(`app-change-hidden-${eventTargetOnlyId}`);
    //     // appChangeHidden.value = "";
    // }

});