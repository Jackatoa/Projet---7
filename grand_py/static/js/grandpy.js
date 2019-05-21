$(function () {
    var $msg_card_body, EntryForm;
    $msg_card_body = $('#msg_card_body');
    EntryForm = $('#EntryForm');
    $("#grandpy_writing").show();
    EntryForm.on('submit', function (e) {
        e.preventDefault();
        var text = $.trim($('#text').val());
        if (text.trim()){$msg_card_body.append('<div class="d-flex justify-content-end mb-4' +
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

        $.post('/bot', {text: text,}).done(function (response) {
            $("#grandpy_writing").hide();
            $msg_card_body.append('<div class="d-flex justify-content-start mb-4" id="grandpy_msg_template">' +
                '<div class="img_cont_msg">' +
            '<img src="../static/images/GrandPy2.png" class="rounded-circle user_img_msg"></div>' +
            '<div class="msg_cotainer">' +
            '<p class="small">' + response['answer'] + '</p>' +
            '</div>' +
            '</div>');
        })



        }

    });


});



