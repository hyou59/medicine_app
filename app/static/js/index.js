// index.htmlで使用

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
        let residue = cells[2].innerHTML;

        // 残量の数値だけを取得
        let residueDay = residue.split("日");
        residueDay = residueDay[0];
        
        // 薬が切れていれば行を赤色で表示
        if (residueDay <= 0) {
            $(cells).css("background-color", "#FFDBC9");

        // 薬が切れる予測日が1週間以内の場合は行を黄色で表示
        } else if (residueDay <= 7) {
            $(cells).css("background-color", "#FFFFBB");
        };

    }
});


$('.dropdown').mouseenter(function(){
    if(!$('.navbar-toggle').is(':visible')) {
        if(!$(this).hasClass('open')) {
        $('.dropdown-toggle', this).trigger('click');
        }
    }
});

