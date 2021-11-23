#! /usr/bin/env nodejs


var iters = document.getElementsByClassName('element left col-md-6').length
var list_elements = document.getElementsByClassName('element left col-md-6')
var act_btn = document.querySelector('#somebutton')

function hideInputs () {
    for (var i=0; i<iters; i++) {
        list_elements[i].toggleAttribute('hidden')
    }
}

act_btn.addEventListener('click', hideInputs)


/*
 *  Get button id and body id compare them in for-loop
 *  so every button with uniq id get assigned same body with
 *  same id
 */
var buttons = document.getElementsByName('button')

function hide(event) {
    idx = event.currentTarget.idx
    list_elements[idx].toggleAttribute('hidden')
}

for (var i = 0; i<iters; i++ ) {
    buttons[i].addEventListener('click', hide)
    buttons[i].idx = i
}
