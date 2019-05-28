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
            $("#msg_card_body").stop().animate({scrollTop: $("#msg_card_body")[0].scrollHeight}, 1000);
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
                    if (big_answer['wiki_answer']) {
                        $msg_card_body.append('<div class="d-flex justify-content-start mb-4" id="grandpy_msg_template">' +
                            '<div class="img_cont_msg">' +
                            '<img src="../static/images/GrandPy2.png" class="rounded-circle user_img_msg"></div>' +
                            '<div class="msg_cotainer">' +
                            '<p class="small">' + big_answer['wiki_answer'] + '</p>' +
                            '</div>' +
                            '</div>');
                    }
                    if (big_answer['map_answer']) {
                        if (document.contains(document.getElementById("mapid"))) {
                            var element = document.getElementById("mapid");
                            element.parentNode.removeChild(element);
                        }
                        $msg_card_body.append('<div class="d-flex justify-content-start mb-4"' +
                            ' id="grandpy_msg_template">' +
                            '<div class="img_cont_msg">' +
                            '<img src="../static/images/GrandPy2.png" class="rounded-circle user_img_msg"></div>' +
                            '<div class="msg_cotainer" id="mapidbox">' +
                            '<p class="small">' + big_answer['map_answer'] + '</p>' +
                            '<div id="mapid">' +
                            '</div>' +
                            '</div>' +
                            '</div>');
                        var mymap = L.map('mapid').setView([big_answer['answer_lat'], big_answer['answer_long']], big_answer['zoom']);
                        L.marker([big_answer['answer_lat'], big_answer['answer_long']]).addTo(mymap);
                        L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
                            attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
                            minZoom: 0,
                            maxZoom: 18,
                            id: 'mapbox.streets',
                            accessToken: 'pk.eyJ1IjoiamFja2F0b2EiLCJhIjoiY2p3MmVwNW5yMDVzbzN5cW55bjVxdWhidCJ9.jtwQWGRlS8_emw5VM23VLg'
                        }).addTo(mymap);
                    }
                    $("#grandpy_writing").hide();
                    playSound()
                    $("#msg_card_body").stop().animate({scrollTop: $("#msg_card_body")[0].scrollHeight}, 1000);
                }, 3000);
            })
        }
    });
});

function playSound() {
    var sound = document.getElementById("audio");
    sound.play();
};
