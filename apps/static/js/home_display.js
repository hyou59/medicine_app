// home.htmlで使用

// 薬が切れる日数を参照して行の色を変える
$(function(){
    //すべての行のデータを配列で取得
    let rows = $("#table1 tbody").children();
    //行数を取得
    let rowsNum= rows.length;

    //1行ずつループ
    for(let i = 0; i < rowsNum; i++){
        //行を取得
        let row = $(rows[i]);
        //セルの配列を取得
        let cells = $(row.children());
        
        // 薬の残量を取得
        let residue = cells[2].textContent;

        // 残量の数値だけを取得
        let residueDay = residue.split("日");
        residueDay = residueDay[0];
        
        // 薬が切れていれば行を赤色で表示
        if (residueDay <= 0) {
            $(cells).css("background-color", "#FFDBC9");

        // 薬が切れる予測日まで1週間以内の場合は行を黄色で表示
        } else if (residueDay <= 7) {
            $(cells).css("background-color", "#FFFFBB");
        };
    }
});


// 削除ボタンの活性・非活性
$(function(){
    // 初期状態のボタンは無効
    $("#del-btn").prop("disabled", true);
    // チェックボックスの状態が変わったら（クリックされたら）
    $("input[type='checkbox']").on('change', function () {
        // チェックされているチェックボックスの数
        if ($(".chk:checked").length > 0) {
            // ボタン有効
            $("#del-btn").prop("disabled", false);
        } else {
            // ボタン無効
            $("#del-btn").prop("disabled", true);
        }
    });
});