var express = require( "express" );
var app = express();
var http = require( "http" );
app.use( express.static( "./public" ) ); // where the web page code goes
var http_server = http.createServer( app ).listen( 3000 );
var http_io = require( "socket.io" )( http_server );

http_io.on( "connection", function( httpsocket ) {
    httpsocket.on( 'python-message', function( fromPython ) {
        httpsocket.broadcast.emit( 'message', fromPython );
    });
});