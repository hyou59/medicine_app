// 処方記録画面のカレンダーに今日の日時を表示
var date = new Date();

var yyyy = date.getFullYear();
var mm = ("0" + (date.getMonth() + 1)).slice(-2);
var dd = ("0" + date.getDate()).slice(-2);

document.getElementById("today").value = yyyy + '-' + mm + '-' + dd;


// 薬の新規登録画面にて読み込み時にセレクトボックスを動的に作成
document.addEventListener('DOMContentLoaded', function() {

    // 飲み薬の数だけ繰り返す
    let selectResidue1 = document.getElementsByName("InternalResidue");
    for (let i = 0; i < selectResidue1.length; i++) {
        let selectElement = selectResidue1[i];

        // セレクトボックス生成
        for (let j = 1; j <= 60; j++) {
            let option = document.createElement('option');
            option.setAttribute("value", j);
            option.textContent = j;
            selectElement.appendChild(option);
            // 初期値を30に設定
            if (j === 30) {
                option.setAttribute("selected", true);
            }
        }
    }

    // 塗り薬の数だけ繰り返す
    let selectResidue2 = document.getElementsByName("ointResidue");
    for (let i = 0; i < selectResidue2.length; i++) {
        let selectElement = selectResidue2[i];

        // セレクトボックス生成
        for (let j = 1; j <= 10; j++) {
            let option = document.createElement('option');
            option.setAttribute("value", j);
            option.textContent = j;
            selectElement.appendChild(option);
            // 初期値を3に設定
            if (j === 3) {
                option.setAttribute("selected", true);
            }
        }
    }
});