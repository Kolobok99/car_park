// 'use strict'

// document.addEventListener('click', function (event) {

//     const evenClassName = event.target.className;
//     // console.log(evenClassName);

//     const input_check_auto = this.getElementById('auto');
//     const input_check_man = this.getElementById('man');

//     const car_title = this.getElementById('opacity-title-car');
//     const man_title = this.getElementById('opacity-title-man');

//     const block_to_hide_car = this.getElementById("block-to_hide-car");
//     const block_to_hide_man = this.getElementById("block-to_hide-man");


//     // Если нажат чек (авто) -> toogle("sub-item_hidy") к отпуск(m)

//     // Если нажата возле label
//         // filtr-items__sub-item
//         // filtr-items__check
    
//     // Если нажат label или check:
//         // filtr-items__check-label
//         // filtr-items__check
    
//     if (input_check_auto.checked) {
//         // console.log('YES!');
//         block_to_hide_man.classList.add('class-to-hide-block');
//         man_title.classList.add('class-to-hide-title');

//     } else {
//         block_to_hide_man.classList.remove('class-to-hide-block');
//         man_title.classList.remove('class-to-hide-title');
//     };

//     if (input_check_man.checked) {
//         // console.log('YES!');
//         block_to_hide_car.classList.add('class-to-hide-block');
//         car_title.classList.add('class-to-hide-title');

//     } else {
//         block_to_hide_car.classList.remove('class-to-hide-block');
//         car_title.classList.remove('class-to-hide-title');

//     };

//     if (input_check_auto.checked && input_check_man.checked) {
//         block_to_hide_man.classList.remove('class-to-hide-block');
//         man_title.classList.remove('class-to-hide-title');
//         block_to_hide_car.classList.remove('class-to-hide-block');
//         car_title.classList.remove('class-to-hide-title');
//     }
    
// });
