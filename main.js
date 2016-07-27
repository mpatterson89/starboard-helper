var express = require('express');
var bodyParser = require('body-parser')
var app = express();

ip = ""

app.use(bodyParser.urlencoded({
    extended: true
}));

/**bodyParser.json(options)
 * Parses the text as JSON and exposes the resulting object on req.body.
 */
app.use(bodyParser.json());



app.set('port', (process.env.PORT || 5000));
app.get('/', function (req, res) {
  	console.log('RECIEVED!!')
	res.send('Starbound Server IP: '+ip);
});

// POST method route
app.post('/', function (req, res) {
  console.log('POST! ',req.body )
  ip = req.body.ip
  res.send('POST request to the homepage');
});

app.listen(app.get('port'), function () {
  console.log('Example app listening on port', app.get('port'));
});
