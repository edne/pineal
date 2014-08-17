
post = function(e) {
    $('.visual').each(function() {
        var visual_name = $(this).children('.visual_name').html();

        $(this).children('.var').each(function() {
            if( $(this).children('.var_value')[0] == e.currentTarget ) {
                var var_name = $(this).children('.var_name').html();
                var var_value = $(this).children('.var_value').val();

                $.post(
                    '/' + visual_name + '/' + var_name,
                    {
                        'value': var_value
                    }
                );
            }

        });

    });
};

add = function(visual_name, var_name) {
    if(!$('#'+visual_name)[0]) {
        $('body').append(
            '<div class="visual" id="'+visual_name+'">\n'+
            '    <span class="visual_name">'+visual_name+'</span>\n'+
            '</div>\n'
        );
    }
    $('#'+visual_name).append(
        '<div class="var" id="'+visual_name+'_'+var_name+'">\n'+
        '    <span class="var_name">'+var_name+'</span>\n'+
        '    <input type="range" min="0" max="1" step="0.02" class="var_value">\n'+
        '</div>'
    );

    $('#'+visual_name+'_'+var_name+' '+' .var_value').bind('change', post);
};

remove = function(visual_name, var_name) {
    $('#'+visual_name+'_'+var_name).remove();

    if(!$('#'+visual_name+' '+'.var')[0]) {
        $('#'+visual_name).remove();
    }
};

// websocket callback
callback = function(e) {
    [action, visual_name, var_name] = e.data.split(' ');
    //console.log(action);
    if(action=='add') {
        add(visual_name, var_name);
    }
    if(action=='remove') {
        remove(visual_name, var_name);
    }
}

polling = function() {
    $.post(
        '/polling',
        function(data) {
            if(data) {
                //console.log(data);
                [action, visual_name, var_name] = data.split(' ');
                if(action=='add') {
                    add(visual_name, var_name);
                }
                if(action=='remove') {
                    remove(visual_name, var_name);
                }
            }
        }
    );
}

$(document).ready(function() {
    setInterval(polling, 100);

    //(new WebSocket("ws://localhost:42080/websocket")).onmessage = callback;
});
