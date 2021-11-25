#! /usr/bin/env nodejs

// Callback function allows to wait until something happens and respond to it

document.addEventListener('keypress', function(event) { console.log(event) } )

var tableToggleButton = document.getElementById('table-toggle')
var inputFields = document.getElementById('input-table')

var addMoreButton = document.getElementById('add-more')
var tableNotDones = document.getElementById('notdones')

function hideNotDones () {
    tableNotDones.classList.toggle('show')
}

function showInputTable () {
    if (inputFields.style.display === 'none') {
        inputFields.style.display = 'flex'
    } else {
        inputFields.style.display = 'none'
    }
}

addMoreButton.addEventListener('click', showInputTable) 
tableToggleButton.addEventListener('click', hideNotDones)


