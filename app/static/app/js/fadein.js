// 画面が読み込まれた時、fade-inクラスを追加しアニメーションさせる
$(window).on('load', function () {
    $('form').addClass('fadein');
});

$(function () {
    // ハッシュリンク(#)と別ウィンドウでページを開く場合は実行しない
    $('a:not([href^="#"]):not([target])').on('click', function (e) {
        e.preventDefault();         // ページ遷移を一旦キャンセル
        url = $(this).attr('href'); // 遷移先のURLを取得
        if (url !== '') {
            $('form').removeClass('fadein'); // 画面遷移前のアニメーション
            setTimeout(function () {
                window.location = url;  // 0.5秒後に取得したURLに遷移
            }, 500);
        }
        return false;
    });
});
