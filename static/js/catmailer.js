$(function() {
    $('#submit-button').on('click', function(e) {
        signup();
    });
    $('#email-input').on('keypress', function(e) {
        if (e.keyCode === 13) {
            signup();
        }
    });
});

function signup() {
    var email = $('#email-input').val();
    if (!email) {
        showMessage('Please enter an email address.', true);
    }
    else if (isValidEmail(email)) {
        //send it to the server
        $('#email-input').prop('disabled', true);
        $('#submit-button').prop('disabled', true);
        $.ajax('/signup', {
            data: {email: email},
            method: 'POST',
            success: function(res) {
                showSuccessView();
            },
            error: function(res) {
                $('#email-input').prop('disabled', false);
                $('#submit-button').prop('disabled', false);
                if (res['responseJSON'] && res['responseJSON']['error']) {
                    var errorMessage = res['responseJSON']['error'];
                    showMessage(errorMessage, true);
                } else {
                    showMessage('Something went wrong on the server. Try again later.', true);
                }
            }
        });
    } else {
        //show error
        showMessage('Please enter a valid email address.', true);
    }
}

function showMessage(message, error) {
    var messageClass = error ? 'error-message' : '';
    $('#error-message-container').html('<span class="' +messageClass + '">' + message + '</span>');
}

function isValidEmail(email) {
    var regex = /^([a-zA-Z0-9_\.\-\+])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    return regex.test(email);
}

function showSuccessView() {
    $('#signup-form').hide();
    $('#success-container').show();
}