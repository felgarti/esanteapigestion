$.ajax({
    url : {% url 'home' %}
    type : "POST", // http method
    data : {
      alerts:"alerts",
      csrfmiddlewaretoken: '{{ csrf_token }}' , //This is must for security in Django
    }, // data sent with the post request

    // handle a successful response
    success : function(response){
      console.log(response["alerts"]);
    },

    // handle a non-successful response
    error : function() {
console.log('error')
    }
});



var socket = new WebSocket('ws://localhost:8001/ws/har/')

    socket.onmessage=function(event){

var data= JSON.parse(event.data);

console.log(data.message);

$.ajax({
    url : '{% url 'home' %}' ,
    type : "POST",
    data : {
      alerts:"{{alerts}}",

    },



}).done(function(response){
console.log("test")
$('#alerts').append(response);
});





    }
