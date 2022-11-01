const setaMostrar1 = document.getElementById('mostrar');
const setaEsconder1 = document.getElementById('esconder');
document.querySelector("#btn1").addEventListener("click", function (event) {
    let value = event.target.getAttribute("aria-expanded");
    if (value == 'true') {
        setaMostrar1.style.display = 'inline';
        setaEsconder1.style.display = 'none';
    }
    else {
        setaMostrar1.style.display = 'none';
        setaEsconder1.style.display = 'inline';
    }
});

const setaMostrar2 = document.getElementById('mostrar2');
const setaEsconder2 = document.getElementById('esconder2');
document.querySelector("#btn2").addEventListener("click", function (event) {
    let value = event.target.getAttribute("aria-expanded");
    if (value == 'true') {
        setaMostrar2.style.display = 'inline';
        setaEsconder2.style.display = 'none';
    }
    else {
        setaMostrar2.style.display = 'none';
        setaEsconder2.style.display = 'inline';
    }
});

const setaMostrar3 = document.getElementById('mostrar3');
const setaEsconder3 = document.getElementById('esconder3');
document.querySelector("#btn3").addEventListener("click", function (event) {
    let value = event.target.getAttribute("aria-expanded");
    if (value == 'true') {
        setaMostrar3.style.display = 'inline';
        setaEsconder3.style.display = 'none';
    }
    else {
        setaMostrar3.style.display = 'none';
        setaEsconder3.style.display = 'inline';
    }
});

const setaMostrar4 = document.getElementById('mostrar4');
const setaEsconder4 = document.getElementById('esconder4');
document.querySelector("#btn4").addEventListener("click", function (event) {
    let value = event.target.getAttribute("aria-expanded");
    if (value == 'true') {
        setaMostrar4.style.display = 'inline';
        setaEsconder4.style.display = 'none';
    }
    else {
        setaMostrar4.style.display = 'none';
        setaEsconder4.style.display = 'inline';
    }
});

const setaMostrar5 = document.getElementById('mostrar5');
const setaEsconder5 = document.getElementById('esconder5');
document.querySelector("#btn5").addEventListener("click", function (event) {
    let value = event.target.getAttribute("aria-expanded");
    if (value == 'true') {
        setaMostrar5.style.display = 'inline';
        setaEsconder5.style.display = 'none';
    }
    else {
        setaMostrar5.style.display = 'none';
        setaEsconder5.style.display = 'inline';
    }
});

function fechar() {
    const btnClose1 = document.getElementById('collapseOne');
    btnClose1.classList.remove('show');
    setaMostrar1.style.display = 'inline';
    setaEsconder1.style.display = 'none';

    const btnClose2 = document.getElementById('collapseTwo');
    btnClose2.classList.remove('show');
    setaMostrar2.style.display = 'inline';
    setaEsconder2.style.display = 'none';

    const btnClose3 = document.getElementById('collapseThree');
    btnClose3.classList.remove('show');
    setaMostrar3.style.display = 'inline';
    setaEsconder3.style.display = 'none';

    const btnClose4 = document.getElementById('collapseFour');
    btnClose4.classList.remove('show');
    setaMostrar4.style.display = 'inline';
    setaEsconder4.style.display = 'none';

    const btnClose5 = document.getElementById('collapseFive');
    btnClose5.classList.remove('show');
    setaMostrar5.style.display = 'inline';
    setaEsconder5.style.display = 'none';
}