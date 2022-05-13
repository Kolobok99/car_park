"use strict"
//wrapper
const wrapper = document.getElementsByClassName('wrapper')[0];
//формы изменения заявки:
const formAddCard = document.getElementsByClassName('form-card add')[0];

document.addEventListener('click', function (event) {

    const evenClassName = event.target.className;
    // Кнопка отправки запроса фильтрации
    const filterButton =  this.getElementsByClassName('filtr-items__button')[0];
    // check 'Есть водитель'
    const OwnerYES = this.getElementById("yes")
    // Нет водителя
    const OwnerNO = this.getElementById("no")

    // Блокировка кнопки
    if ( !OwnerYES.checked && !OwnerNO.checked ){
        filterButton.disabled=true;
        filterButton.style.opacity=0.5;
    } else {
        filterButton.disabled=false;
        filterButton.style.opacity=1;
    }


    //кнопка открытия формы (добавления карт):
    const btnAddCard = this.getElementsByClassName('main__btn-add-card')[0];
    //кнопка закрытия формы (добавления карт):
    const btnResetCardAdd = document.getElementsByClassName('bnt-form-card-reset-add')[0];

    if (evenClassName === btnAddCard.className || btnResetCardAdd.contains(event.target)) {
        formAddCard.classList.toggle('data-show-or-hide-form');
        wrapper.classList.toggle('blackout');
    }
    // Cообщение
     const message_box = this.getElementsByClassName('messages')[0];
    // Кнопка закрытия сообщения:
    const message_close = this.getElementsByClassName('close')[0];

    // Закрытие сообщения
     if (evenClassName === message_close.className){
        message_box.style.display = "none"
    }
});

const errorList = document.getElementsByClassName("errorlist");
if (errorList.length !== 0) {
        formAddCard.classList.add('data-show-or-hide-form');
        wrapper.classList.add('blackout');
    }


