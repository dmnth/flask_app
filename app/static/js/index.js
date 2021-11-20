#! /usr/bin/env nodejs

var numberOfIters = document.querySelectorAll('.sort').length;

for (var i = 0; i<2; i++) {

    document.querySelectorAll('.sort')[i].addEventListener('click', function () {
        this.style.color='red';
        this.style.background='green';
    });
}

var gateKeeper = {
    age: 'unknown',
    name: 'Banglasheumns',
    circle: 'gluttony',
    souls: 1299938,
    hobby: 'kittens',
}

/* Constructor function - names has to be capitalized */

function delegateSouls () {
    alert('12 souls have been delegeted to inner circle')
}

function GateKeeper(age, name, circle, souls, hobby) {
    this.age = age;
    this.name = name;
    this.circle = circle;
    this.souls = souls;
    this.hobby = hobby;
    this.punish = function () {alert('punishments in progress')}
    this.delegateSouls = delegateSouls
}

/* Object initialization */

var gateKeeper2 = new GateKeeper('over9000', 'Fraudenius', 'blashphemy', 99322130, 'jogging');


