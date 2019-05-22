$(function () {
    var $msg_card_body, EntryForm;
    $msg_card_body = $('#msg_card_body');
    EntryForm = $('#EntryForm');
    $("#grandpy_writing").hide();
    EntryForm.on('submit', function (e) {
        e.preventDefault();
        var text = $.trim($('#text').val());
        text = text.split('<').join('&lt;');
        text = text.split('>').join('&gt;');
        if (text.trim()) {
            $msg_card_body.append('<div class="d-flex justify-content-end mb-4' +
                ' main_user_img" id="user_msg_template">' +
                '<div class="msg_cotainer_send">' +
                '<p class="small">' + text + '</p>' +
                '</div>' +
                '<div class="img_cont_msg">' +
                '<img src="../static/images/GrandSon.png"' +
                ' class="rounded-circle user_img_msg">' +
                '</div>' +
                '</div>');
            $.trim($('#text').val(''));
            var pageHeight = $('#msg_card_body').height();
            $('#msg_card_body').scrollTop(pageHeight);

            $.post('/bot', {text: text,}).done(function (big_answer) {
                $("#grandpy_writing").show();
                setTimeout(function () {
                    $msg_card_body.append('<div class="d-flex justify-content-start mb-4" id="grandpy_msg_template">' +
                        '<div class="img_cont_msg">' +
                        '<img src="../static/images/GrandPy2.png" class="rounded-circle user_img_msg"></div>' +
                        '<div class="msg_cotainer">' +
                        '<p class="small">' + big_answer['answer'] + '</p>' +
                        '</div>' +
                        '</div>');
                    $("#grandpy_writing").hide();
                    playSound()
                    var pageHeight = $('#msg_card_body').height();
                    $('#msg_card_body').scrollTop(pageHeight);
                }, 3000);

            })
        }
    });
});


function playSound() {
    var sound = document.getElementById("audio");
    sound.play();
}
