$(document).ready(function() {
    var login = true;
    var signup = false;
    $('#const_btn1').click(function() {
        if (login === false) {

            $('#sigupdiv').css('display', 'none');
            $('#logindiv').css('display', 'grid');
            login = true;
            signup = false;

        }

    });
    $('#const_btn2').click(function() {
        if (signup === false) {
            $('#logindiv').css('display', 'none');
            $('#sigupdiv').css('display', 'grid');
            signup = true;
            login = false;

        }

    });

    $('.loginbtn').mouseenter(function() {


        $(this).css('background-color', 'rgb(23, 157, 202)');



    });
    $('.loginbtn').mouseleave(function() {


        $(this).css('background-color', 'rgb(99, 197, 230)');



    });
    $('.signupbtn').mouseenter(function() {


        $(this).css('background-color', 'rgb(23, 157, 202)');



    });
    $('.signupbtn').mouseleave(function() {


        $(this).css('background-color', 'rgb(99, 197, 230)');



    });
    var firstp = '';
    var secondp = '';


    $('.i1').blur(function() {
        firstp = $(this).val();
        if (firstp.trim()) {

            if (firstp.trim().length < 8) {
                alert('password length must be equal or graterthan 8');
                $(this).val('');
            }

        }

    });

    $('.i2').blur(function() {

        secondp = $(this).val();

        if (secondp.trim()) {

            if (firstp.trim()) {
                if (firstp.trim() != secondp.trim()) {
                    alert('passwrods not match');
                    $(this).val('');

                }
            }

        }

    });






})