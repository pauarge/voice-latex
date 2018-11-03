const path = require('path');
const fs = require('fs');
const express = require('express');
const app = express();
const http = require('http').Server(app);
const io = require('socket.io')(http);

app.use('/static', express.static(path.join(__dirname, 'public')))

app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');
});

app.get('/update', (req, res) => {
    fs.readFile('./public/generated.tex', 'utf8', (err, contents) => {
        io.emit('update', contents);
    });
    res.json({'status': 'ok'});
});

io.on('connection', function (socket) {
    console.log('a user connected');
    socket.on('disconnect', function () {
        console.log('user disconnected');
    });
});

http.listen(3000, function () {
    console.log('listening on *:3000');
});
