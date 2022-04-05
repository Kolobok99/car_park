"use strict"

document.addEventListener('click', function (event) {

    const evenClassName = event.target.className;
    const wrapper = document.getElementsByClassName('wrapper')[0];
    
    //Работа с формой редактирования
    
    //кнопка открытия формы:
    const btnChangeApp = this.getElementsByClassName('info-app__btn-submit')[0];
    
    //формы изменения заявки:
    const formChange = this.getElementsByClassName('form-app change')[0];

    //кнопка закрытия формы btnReset
    const btnResetAppChange = document.getElementsByClassName('bnt-form-app-reset-change')[0];


    if (evenClassName == btnChangeApp.className || btnResetAppChange.contains(event.target)) {
        formChange.classList.toggle('data-show-or-hide-form');
        wrapper.classList.toggle('blackout');
    };
});