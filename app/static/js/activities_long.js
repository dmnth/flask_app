#! /usr/bin/env nodejs

var element = document.querySelector('#add-stuff-top')
var btn = document.querySelector('button.btn.btn-dark')

function hideInput () {
    element.toggleAttribute('hidden')
}

btn.addEventListener('click', hideInput)
