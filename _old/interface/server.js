var fs = require('fs');
var http = require('http');
var https = require('https');
var privateKey  = fs.readFileSync(__dirname +'/key.pem', 'utf8');
var certificate = fs.readFileSync(__dirname +'/cert.pem', 'utf8');
var passpass= "niquetout"
var credentials = {key: privateKey, cert: certificate, passphrase : passpass};
var express = require('express');
var app = express();
var path = require('path');
var swig = require('swig');
var bodyParser = require('body-parser');
var gulp = require('gulp');


var portUsed = 3000;
var portSecureUsed = 4000;

var httpServer = http.createServer(app);
var httpsServer = https.createServer(credentials, app);
console.log("listening http on: "+portUsed)
console.log("listening https on: "+portSecureUsed)

var allowCrossDomain = function(req, res, next) {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE');
    res.header('Access-Control-Allow-Headers', 'Content-Type');
    next();
}

app.use(allowCrossDomain);


// For http
httpServer.listen(portUsed);
// For https
httpsServer.listen(portSecureUsed);

/* file for interface */
app.use(express.static(path.join(__dirname, './public/client')));
/* file with state update by python */
app.use(express.static(path.join(__dirname, '../bridge')));
/* file with capture done by python */
app.use(express.static(path.join(__dirname, '../capture')));

app.engine('html', swig.renderFile);

app.set('view engine', 'html');

app.get('/step', function(req,res){
  var state  = fs.readFileSync("/home/pi/Desktop/huuurlomaton/bridge/share-python-data.txt", 'utf8');
  console.log(state);
  res.setHeader('Content-Type', 'application/txt');
  res.send(( state ));
});

app.get('/*', function(req,res){
 res.render(__dirname + '/public/client/index');
});
