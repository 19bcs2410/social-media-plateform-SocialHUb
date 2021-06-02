var socket = io();
socket.on('connect', function() {
    console.log('connected');
});
var username1 = '';
socket.on('e1', function(data) {
    username1 = data['data'];

});