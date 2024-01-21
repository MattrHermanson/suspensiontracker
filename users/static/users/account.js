
const tabs = ["body1", "body2"];

function hideAll(tabList) {
    for (let i = 0; i < tabList.length; i++) {
        document.getElementById(tabList[i]).style.display = 'none';
    }
}


// tab switch function

function showTab(tabNum) {
    hideAll(tabs)
    document.getElementById("body"+tabNum).style.display = 'block';
}

