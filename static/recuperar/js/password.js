$(document).ready(function() {
    var showPassword = false;

    $('.show-password-icon1').mousedown(function() {
        showPassword = true;
        var passwordInput = $(this).siblings('input');
        passwordInput.attr('type', 'text');
    });

    $(document).mouseup(function() {
        if (showPassword) {
            showPassword = false;
            var passwordInput = $('.show-password-icon1').siblings('input');
            passwordInput.attr('type', 'password');
        }
    });
});
$(document).ready(function() {
    var showPassword = false;

    $('.show-password-icon2').mousedown(function() {
        showPassword = true;
        var passwordInput = $(this).siblings('input');
        passwordInput.attr('type', 'text');
    });

    $(document).mouseup(function() {
        if (showPassword) {
            showPassword = false;
            var passwordInput = $('.show-password-icon2').siblings('input');
            passwordInput.attr('type', 'password');
        }
    });
});