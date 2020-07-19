var drawGraph = function (data_x, data_y, type_chart) {
    // グラフの最大値を推定
    var itemMax = Math.max.apply(null, data_y);
    var index = Math.floor(Math.log10(itemMax));
    itemMax = Math.ceil(itemMax / 10 ** index) * 10 ** index;
    // グラフの描画
    var outgoCanvas = document.getElementById("outgoCanvas");
    var ctx = outgoCanvas.getContext('2d');

    Chart.defaults.global.defaultFontColor = 'black';
    Chart.defaults.global.defaultFontSize = 18;
    Chart.defaults.global.defaultFontStyle = "bold";
    Chart.defaults.global.defaultFontFamily = "Arial";

    window.mainChart = new Chart(ctx, {
        type: type_chart,
        data: {
            labels: [...data_x],
            datasets: [{
                label: "A",
                data: [...data_y],

                backgroundColor: 'rgba(110,121,92,0.1)',
                borderColor: 'rgba(110,121,92,1)',
                lineTension: 0,

                pointRadius: 10,
                pointHitRadius: 15,
                pointBackgroundColor: 'rgba(110,121,92,1)',
                pointBorderColor: 'rgba(110,121,92,1)',
            },
            ]
        },
        options: {
            title: {
                display: false,
                text: 'グラフ'
            },
            legend: {
                display: false
            },
            scales: {
                xAxes: [
                    {
                        gridLines: {
                            color: 'rgba(166, 177, 147, 1)',
                            lineWidth: 4,
                            borderDash: [4, 1],
                        }
                    }
                ],
                yAxes: [
                    {
                        gridLines: {
                            color: 'rgba(166, 177, 147, 1)',
                            zeroLineColor: 'rgba(166, 177, 147, 1)',
                            borderDash: [2, 1],
                        },
                        ticks: {
                            suggestedMax: itemMax + 1,
                            suggestedMin: 0, // 要改善
                            stepSize: itemMax / 2, // 適当
                            callback: function (value, index, values) {
                                return value // + '円'
                            }
                        }
                    }
                ],
            },
        }
    });
    // グラフの点をクリックした際の処理を追加
    outgoCanvas.onclick = function (e) {
        var item = mainChart.getElementAtEvent(e);
        if (!item.length) return; // return if not clicked on slice
        var index = item[0]._index;
        $(".popup-overlay, .popup-content, .popup-background").addClass("active");
        $.ajax({
            url: '/api/item/get',
            type: 'GET',
            data: {
                'point_id': index,
            }
        }).done(response => {
            var itemList = response.itemList
            // jQueryによるパターン
            $("#popup-date").html("");
            target = $("#popup-date");
            text = "<h2>" + item[0]._xScale.ticks[index] + "</h2>";
            $(target).append(text);

            $("#popup-table").html("");
            target = $("#popup-table")
            var text = '<table class="table"><tr><th>日付</th><th>金額</th><th>大カテゴリ</th><th>小カテゴリ</th></tr>';
            var line = '';
            for (var n in itemList) {
                line = line + "<tr><td>" + itemList[n].item + "</td><td>" + itemList[n].price + "</th><td>" + itemList[n].big_category + "</td><td>" + itemList[n].small_category + "</td></tr>";
            }
            text = text + line + '</table>';
            $(target).append(text);
        });
    }
};

var reflectChanges = function (ajax_response, type_chart) {
    // グラフを更新
    var x = [];
    var y = [];
    var month_total = ajax_response.month_total
    for (const tmp of month_total) {
        x.push(tmp.month);
        y.push(tmp.total);
    }
    drawGraph(x, y, type_chart = type_chart);
    // テーブルを更新
    $("#graph-table").html("");
    target = $("#graph-table");
    text = "<table class='table'>\n<tr>\n<th>日付</th>\n<th>金額</th>\n</tr>\n";
    var line = '';
    for (const tmp of month_total) {
        line = line + "<tr>\n<td>" + tmp.month + "</td>\n<td>" + tmp.total + "</td>\n</tr>\n";
    }
    text = text + line + "</table>";
    $(target).append(text);
};