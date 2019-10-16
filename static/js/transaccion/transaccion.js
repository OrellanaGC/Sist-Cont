$(document).ready(function(){
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

    $("#test").submit(function (event){
        $.ajax({
            headers: { "X-CSRFToken": csrftoken }, 
            type: 'POST',
            url: 'nueva/',
            data: {
                'texto' : $("#texto").val(),
                csrfmiddlewaretoken: csrftoken,
            },
            success: function (data){
                alert(data.mensaje);
                for(i = 0; i < data.transacciones.length; i++){
                    console.log(data.transacciones[i].tipo)
                }
                console.log(data);
            }
        });
        return false;
    });

});