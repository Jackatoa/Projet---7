
$(function() {
    var imageurl = "{{ url_for('static', filename='images/GrandSon.png') }}";
  var $msg_card_body, EntryForm;
  $msg_card_body = $('#msg_card_body');
  EntryForm = $('#EntryForm');

  EntryForm.on('submit', function(e) {
    e.preventDefault();
    var text = $.trim($('#text').val());
    $msg_card_body.append('<div class="d-flex justify-content-end mb-4 main_user_img" id="user_msg_template">' +
    '<div class="msg_cotainer_send">' +
        '<p class="small user_msg_1">' + text + '</p>' +
    '</div>' +
    '<div class="img_cont_msg">' +
        '<img src="../static/images/GrandSon.png"' +
      ' class="rounded-circle user_img_msg">' +
    '</div>' +
'</div>');
    $.trim($('#text').val(''));
  });



});



