// 薬の種類により表示：非表示切り替え

// 表示・非表示設定
function medicineChange() {
    // ちらつき解消のために後から画面表示
    $('#select-medicine').fadeIn(0);

    radio = document.getElementsByName('mediType')
    if (radio[0].checked) {
        // 飲み薬選択時に塗り薬の残量設定を非表示
        document.getElementById('firstBox').style.display = "block";
        document.getElementById('secondBox').style.display = "none";
        document.getElementById('thirdBox').style.display = "none";
    }
    else {
        // 塗り薬選択時に飲み薬の残量設定を非表示
        document.getElementById('firstBox').style.display = "none";
        document.getElementById('secondBox').style.display = "block";
        document.getElementById('thirdBox').style.display = "block";
    }
}

window.addEventListener("load", medicineChange);