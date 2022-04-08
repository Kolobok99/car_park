'use strict'

document.addEventListener('click', function (event) {

    const evenClassName = event.target.className;

    const check_auto = this.getElementById('auto');
    const label_to_hidden = this.getElementsByClassName('data-label');
    
    console.log(evenClassName);
    // if (check_auto.checked) {
    //     label_to_hidden.classList.toggle('sub-item_hidy');
    // }


});
