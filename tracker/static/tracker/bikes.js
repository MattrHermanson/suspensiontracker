
window.addEventListener("click", function (event) {
    if (event.target == myPopup) {
        myPopup.classList.remove("show");
    }
});

function popup(){
    myPopup.classList.add("show");
}

function popupClose(){
    myPopup.classList.remove("show");
}