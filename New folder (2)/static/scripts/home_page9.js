$(document).ready(function() {

    console.log(username1);
    $('#header_profile_img1').attr('src', `{{url_for('static',filename='contents/${username1}.jpg')}}`)




    var mystr = '';

    var send_button = $('#sendbtn');
    send_button.mouseenter(function() {
        $(this).css({
            'background-color': 'rgb(8, 121, 187)'
        });

    });
    send_button.mouseleave(function() {
        $(this).css({
            'background-color': 'rgb(175, 214, 236)'
        });

    });
    send_button.click(function() {
        var msg = $('#inputbox').val().trim();



        if (msg.length > 0) {
            var new_node = $('<div id=\'rightmsg\'></div>').html(`${msg}`);
            $('#msgbox').append(new_node);

            $('#inputbox').val('');
            mystr = '';
        }


    });


    $('#msgbox').click(function() {
        $('#emojis').hide();
    });






    $('#inputbox').focus(function() {


        $(this).keypress(function(ev) {
            if (ev.keyCode === 13) {

                var msg = $('#inputbox').val().trim();

                if (msg.length > 0) {
                    var new_node = $('<div id=\'rightmsg\'></div>').html(` <span class='username'>username</span>
                    <span class='message'>${msg}</span>
                    
                    </span>`);
                    $('#msgbox').append(new_node);

                    $('#inputbox').val('');
                    $('#msgbox').scrollTop($('#msgbox')[0].scrollHeight);
                    mystr = '';



                }

            }
        })
    });

    $('#emojibtn').click(function() {

        $('#emojis').toggle();

    });

    $('#sender_img').click(function() {
        $('#zoom_div').slideToggle();

    });

    $('#msgbox').click(function() {
        $('#zoom_div').hide();
    });




    $('button').click(function() {

        console.log(($('#inputbox').val()));


        if ($(this).attr('id') === 'emojibtn_select') {


            //emoji_selected.push($(this).text());
            var mystr1

            if ($('#inputbox').val().trim().length > 0) {
                mystr1 = $('#inputbox').val().trim();
                mystr = '';
            }

            mystr += $(this).text();

            if (mystr1 == undefined) {
                mystr = '' + mystr;

            } else {

                mystr = mystr1 + mystr;

            }






            $('#inputbox').val(mystr);

        }


    });

    $('div').click(function() {
        if ($(this).attr('id') === 'friend_card') {



            $('#sender_name').text($(`h1.${$(this).attr('class')}`).text());
            $('#sender_img').attr('src', $(`img.${$(this).attr('class')}`).attr('src'));
        }
    });











})