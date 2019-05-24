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
                        $msg_card_body.append('<div class="d-flex justify-content-start mb-4" id="grandpy_msg_template">' +
                            '<div class="img_cont_msg">' +
                            '<img src="../static/images/GrandPy2.png" class="rounded-circle user_img_msg"></div>' +
                            '<div class="msg_cotainer">' +
                            '<p class="small">' + big_answer['wiki_answer'] + '</p>' +
                            '</div>' +
                            '</div>');

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
var lat = 48.852969;
var lon = 2.349903;
var macarte = null;

// Fonction d'initialisation de la carte
function initMap() {
    // Créer l'objet "macarte" et l'insèrer dans l'élément HTML qui a l'ID "map"
    macarte = L.map('map').setView([lat, lon], 11);
    // Leaflet ne récupère pas les cartes (tiles) sur un serveur par défaut. Nous devons lui préciser où nous souhaitons les récupérer. Ici, openstreetmap.fr
    L.tileLayer('https://{s}.tile.openstreetmap.fr/osmfr/{z}/{x}/{y}.png', {
        // Il est toujours bien de laisser le lien vers la source des données
        attribution: 'données © <a href="//osm.org/copyright">OpenStreetMap</a>/ODbL - rendu <a href="//openstreetmap.fr">OSM France</a>',
        minZoom: 1,
        maxZoom: 20
    }).addTo(macarte);
}

window.onload = function () {
    // Fonction d'initialisation qui s'exécute lorsque le DOM est chargé
    initMap();
};
