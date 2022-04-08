'use strict'

document.addEventListener('click', function (event) {

    const evenClassName = event.target.className;
    // console.log(evenClassName);

    const input_check_auto = this.getElementById('auto');
    const input_check_man = this.getElementById('man');

    const car_title = this.getElementById('opacity-title-car');
    const man_title = this.getElementById('opacity-title-man');

    const block_to_hide_car = this.getElementById("block-to_hide-car");
    const block_to_hide_man = this.getElementById("block-to_hide-man");


    // Если нажат чек (авто) -> toogle("sub-item_hidy") к отпуск(m)

    // Если нажата возле label
        // filtr-items__sub-item
        // filtr-items__check
    
    // Если нажат label или check:
        // filtr-items__check-label
        // filtr-items__check
    
    if (evenClassName == input_check_auto.className) {
        // console.log('YES!');
        block_to_hide_man.classList.toggle('class-to-hide-block');
        man_title.classList.toggle('class-to-hide-title');

    } else if (evenClassName == input_check_man.className) {
        // console.log('YES!');
        block_to_hide_car.classList.toggle('class-to-hide-block');
        car_title.classList.toggle('class-to-hide-title');

    };
    // if (input_check_auto.checked && input_check_man.checked) {
    //     block_to_hide_man.classList.toggle('class-to-hide-block');
    //     man_title.classList.toggle('class-to-hide-title');
    //     block_to_hide_car.classList.toggle('class-to-hide-block');
    //     car_title.classList.toggle('class-to-hide-title');
    // }
    
});
