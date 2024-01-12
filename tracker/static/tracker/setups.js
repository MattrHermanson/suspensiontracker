
window.addEventListener("click", function (event) {
    if (event.target == myPopup) {
        myPopup.classList.remove("show");
    }
    if (event.target == myPopup2) {
        myPopup2.classList.remove("show");
    }
    if (event.target == myPopup3) {
        myPopup3.classList.remove("show");
    }
    if (event.target == myPopup4) {
        myPopup4.classList.remove("show");
    }
    if (event.target == myPopup5) {
        myPopup5.classList.remove("show");
    }
});

function popup(){
    myPopup.classList.add("show");
}

function popup2(){
    myPopup2.classList.add("show");
}

function popup3(){
    myPopup3.classList.add("show");
}

function popup4(){
    myPopup4.classList.add("show");
}

function popup5(){
    myPopup5.classList.add("show");
}


function popupClose(){
    myPopup.classList.remove("show");
}

function popupClose2(){
    myPopup2.classList.remove("show");
}

function popupClose3(){
    myPopup3.classList.remove("show");
}

function popupClose4(){
    myPopup4.classList.remove("show");
}

function popupClose5(){
    myPopup5.classList.remove("show");
}



function showEditButton() {
    document.getElementById('edit-setup-button').style.display = 'block';
}

function hideEditButton() {
    document.getElementById('edit-setup-button').style.display = 'none';
}
