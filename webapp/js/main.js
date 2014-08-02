
post = function(e) {
    $('.visual').each(function() {
        var visual_name = $(this).children('.visual_name').html();

        $(this).children('.var').each(function() {
            var var_name = $(this).children('.var_name').html();
            var var_value = $(this).children('.var_value').val();

            $.post(
                '/' + visual_name + '/' + var_name,
                {
                    'value': var_value
                }
            );

        });

    });
};

poll = function() {
    /*
    setTimeout(
        function() {
            $.ajax({
                url: 'http://localhost:42080/',
                success: function(data) {
                    alert(data);
                },
                dataType: 'json',
                complete: 'poll'
            });
        },
        30000
    );
    */
    /*
    $.ajax({
        url: 'http://127.0.0.1:42080/',
        success: function(data) {
            alert('ok');
            //poll();
        },
        dataType: 'json',
        complete: 'poll'
    });
    */

}

$(document).ready(function() {
    $('.var_value').bind('change', post);
    poll();
});

