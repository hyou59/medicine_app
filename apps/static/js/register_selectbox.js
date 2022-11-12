// 薬の新規登録画面にて読み込み時にセレクトボックスを動的に作成
document.addEventListener('DOMContentLoaded', function() {

    // 飲み薬の残量のセレクトボックス生成
    let selectResidue1 = document.getElementById("selectResidue1");
    for (let i = 0; i <= 60; i++) {
        let option = document.createElement('option');
        option.setAttribute("value", i);
        option.textContent = i;
        selectResidue1.appendChild(option);
        // 初期値を30に設定
        if (i === 30) {
            option.setAttribute("selected", true);
        }
    }

    // 塗り薬の残量のセレクトボックス生成
    let selectResidue2 = document.getElementById("selectResidue2");
    for (let i = 0; i <= 10; i++) {
        let option = document.createElement('option');
        option.setAttribute("value", i);
        option.textContent = i;
        selectResidue2.appendChild(option);
        // 初期値を3に設定
        if (i === 3) {
            option.setAttribute("selected", true);
        }
    }

    // 塗り薬の1本当たりの使用可能日数のセレクトボックス生成
    let selectOin = document.getElementById("selectOin");
    for (let i = 0; i <= 30; i++) {
        let option = document.createElement('option');
        option.setAttribute("value", i);
        option.textContent = i;
        selectOin.appendChild(option);
        // 初期値を10に設定
        if (i === 10) {
            option.setAttribute("selected", true);
        }
    }
});