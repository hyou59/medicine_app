//カレンダーを生成

// Webページの読み込みが完了したとき
document.addEventListener('DOMContentLoaded', function() {
    let calendarEl = document.getElementById('calendar');
    let calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        // ヘッダー設定
        headerToolbar: {
            left: "",
            center: "title",
        },
        locale: "ja",
        // 日付を選択可
        selectable: true,

        select: function (info) {
            // 入力ダイアログ
            const eventName = prompt("イベントを入力してください");
            
            if (eventName) {
                // イベントの追加
                calendar.addEvent({
                    title: eventName,
                    start: info.start,
                    end: info.end,
                    allDay: true,
                });
            }
        }
    });
    calendar.render();
    });
