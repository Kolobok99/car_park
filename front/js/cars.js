"use strict"

document.addEventListener('click', function (event) {

    const evenClassName = event.target.className;
    const wrapper = document.getElementsByClassName('wrapper')[0];


    //Работа с формой добавления документов:
    
    //кнопка открытия формы:
    const btnAddDoc = this.getElementsByClassName('main__btn-add-car')[0];

     //формы изменения заявки:
    const formAddDoc = this.getElementsByClassName('form-car add')[0];
    
    //кнопка закрытия формы btnReset
    const btnResetDocAdd = document.getElementsByClassName('bnt-form-car-reset-add')[0];

    if (evenClassName == btnAddDoc.className || btnResetDocAdd.contains(event.target)) {
        formAddDoc.classList.toggle('data-show-or-hide-form');
        wrapper.classList.toggle('blackout');
    };    

    
    // if (evenClassName == 'table__btn-add-app') {
    //     formAdd.classList.toggle('data-show-or-hide-form');
    //     wrapper.classList.toggle('overlay');
    // } else if (btnReset.contains(event.target)) {   
    //     console.log('YES!');
    //     formAdd.classList.toggle('data-form-add');
    //     wrapper.classList.toggle('overlay');
    // } else if (evenClassName == 'table__btn-change-app') {

    // }
});