'use strict'
document.addEventListener('click', function (event) {

        const evenClassName = event.target.className;

        // Кнопка отправки запроса фильтрации
        const filterButton =  this.getElementsByClassName('filtr-items__button')[0];

        // checked 'Авто'
        const input_check_auto = this.getElementById('auto');
        // checked 'Авто'
        const input_check_man = this.getElementById('man');

        // Заголовок фильтра "тип (Авто)"
        const car_title = this.getElementById('opacity-title-car');
        // Заголовок фильтра "тип (Человек)"
        const man_title = this.getElementById('opacity-title-man');

        // div с условиями фильтрации типов "авто"
        const block_to_hide_car = this.getElementById("block-to_hide-car");
        // div с условиями фильтрации типов "человек"
        const block_to_hide_man = this.getElementById("block-to_hide-man");


         // Если нажата авто
        if (input_check_auto.checked) {
            // console.log('YES!');
            block_to_hide_man.classList.add('class-to-hide-block');
            man_title.classList.add('class-to-hide-title');
            filterButton.disabled=false;
            filterButton.style.opacity=1;

        } else if (!input_check_auto.checked) {
            block_to_hide_man.classList.remove('class-to-hide-block');
            man_title.classList.remove('class-to-hide-title');

        }
        // Если нажата водитель
        if (input_check_man.checked) {
            // console.log('YES!');
            block_to_hide_car.classList.add('class-to-hide-block');
            car_title.classList.add('class-to-hide-title');
            filterButton.disabled=false;
            filterButton.style.opacity=1;

        } else if (!input_check_man.checked) {
            block_to_hide_car.classList.remove('class-to-hide-block');
            car_title.classList.remove('class-to-hide-title');
        }
         // Если нажата водитель и авто
        if (input_check_auto.checked && input_check_man.checked) {
            block_to_hide_man.classList.remove('class-to-hide-block');
            man_title.classList.remove('class-to-hide-title');
            block_to_hide_car.classList.remove('class-to-hide-block');
            car_title.classList.remove('class-to-hide-title');
            filterButton.disabled=false;
            filterButton.style.opacity=1;
        }
        else if  (!input_check_auto.checked && !input_check_man.checked) {
            block_to_hide_man.classList.add('class-to-hide-block');
            man_title.classList.add('class-to-hide-title');
            block_to_hide_car.classList.add('class-to-hide-block');
            car_title.classList.add('class-to-hide-title');
            filterButton.disabled=true;
            filterButton.style.opacity=0.5;
        }
    }
)



