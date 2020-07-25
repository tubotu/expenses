const drawGraph = function (data_x, data_y, type_chart) {
    // グラフの最大値を推定
    let itemMax = Math.max.apply(null, data_y);
    const index = Math.floor(Math.log10(itemMax));
    itemMax = Math.ceil(itemMax / 10 ** index) * 10 ** index;
    // グラフの描画
    const outgoCanvas = document.getElementById("outgoCanvas");
    const ctx = outgoCanvas.getContext('2d');

    const current_font_size = Number($('.flex').css('font-size').replace(/[^0-9]/g, ''));
    Chart.defaults.global.defaultFontColor = 'black';
    Chart.defaults.global.defaultFontSize = current_font_size;
    Chart.defaults.global.defaultFontStyle = "bold";
    // Chart.defaults.global.defaultFontFamily = "Arial";

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
            layout: {
                padding: {
                    top: 10,
                    bottom: 10,
                }
            },
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
                        },
                        ticks: {
                            padding: 20,
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
                            padding: 20,
                            suggestedMax: itemMax + 1,
                            suggestedMin: 0, // 要改善
                            stepSize: itemMax / 2, // 適当
                            callback: function (value, index, values) {
                                return value + '円'
                            }
                        }
                    }
                ],
            },
        }
    });
    // グラフの点をクリックした際の処理を追加
    outgoCanvas.onclick = function (e) {
        const item = mainChart.getElementAtEvent(e);
        if (!item.length) return; // return if not clicked on slice
        const index = item[0]._index;
        $(".popup-overlay, .popup-content, .popup-background").addClass("active");
        $.ajax({
            url: '/api/item/get',
            type: 'GET',
            data: {
                'point_id': index,
            }
        }).done(response => {
            const itemList = response.itemList
            // jQueryによるパターン
            $("#popup-date").html("");
            target = $("#popup-date");
            text = "<h2>" + item[0]._xScale.ticks[index] + "</h2>";
            $(target).append(text);

            $("#popup-table").html("");
            target = $("#popup-table")
            var text = '<table class="table"><tr><th>項目</th><th>金額</th><th>大カテゴリ</th><th>小カテゴリ</th></tr>';
            var line = '';
            for (const n in itemList) {
                line = line + "<tr><td>" + itemList[n].item + "</td><td>" + itemList[n].price + "</th><td>" + itemList[n].big_category + "</td><td>" + itemList[n].small_category + "</td></tr>";
            }
            text = text + line + '</table>';
            $(target).append(text);
        });
    }
};

const reflectChanges = function (ajax_response, type_chart) {
    // グラフを更新
    const x = [];
    const y = [];
    const month_total = ajax_response.month_total
    for (const tmp of month_total) {
        x.push(tmp.month);
        y.push(tmp.total);
    }
    drawGraph(x, y, type_chart = type_chart);
    // テーブルを更新
    $("#graph-table").html("");
    target = $("#graph-table");
    var text = "<table class='table'>";
    var line = '';
    for (const tmp of month_total) {
        line = line + "<tr>\n<td>" + tmp.month + "</td>\n<td>" + tmp.total + "円</td>\n</tr>\n";
    }
    text = text + line + "</table>";
    $(target).append(text);
};