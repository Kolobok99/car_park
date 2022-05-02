"use strict"

document.addEventListener('click', function (event) {

    const evenClassName = event.target.className;
    const wrapper = document.getElementsByClassName('wrapper')[0];

    // //Работа с формой присваивания :

    // //кнопка открытия формы:
    const btnAddCard = this.getElementsByClassName('table__btn-add-card')[0];
    // //форма добавления заявки:
    const formAdd = document.getElementsByClassName('form-card')[0];
    // //кнопка закрытия формы
    const btnResetAppAdd = document.getElementsByClassName('bnt-form-card-reset-add')[0];


    if (evenClassName === btnAddCard.className || btnResetAppAdd.contains(event.target)) {
        formAdd.classList.toggle('data-show-or-hide-form');
        wrapper.classList.toggle('blackout');
    };








});
