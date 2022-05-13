"use strict"

//wrapper
const wrapper = document.getElementsByClassName('wrapper')[0];
//формы добавления машины:
const formAddCar = document.getElementsByClassName('form-car add')[0];

document.addEventListener('click', function (event) {

    const evenClassName = event.target.className;

    //кнопка открытия формы (добавления машины):
    const btnAddCar = this.getElementsByClassName('main__btn-add-car')[0];

    //кнопка закрытия формы btnReset (добавления машины):
    const btnResetCarAdd = document.getElementsByClassName('bnt-form-car-reset-add')[0];

    if (evenClassName === btnAddCar.className || btnResetCarAdd.contains(event.target)) {
        formAddCar.classList.toggle('data-show-or-hide-form');
        wrapper.classList.toggle('blackout');
    }

    const message_box = this.getElementsByClassName('messages')[0];
    // Кнопка закрытия сообщения:
    const message_close = this.getElementsByClassName('close')[0];

      if (evenClassName === message_close.className){
        message_box.style.display = "none"
    }

});

const errorList = document.getElementsByClassName("errorlist");
console.log(errorList.length);
if (errorList.length !== 0) {
    console.log('YES!');
    formAddCar.classList.add('data-show-or-hide-form');
    wrapper.classList.add('blackout');
}