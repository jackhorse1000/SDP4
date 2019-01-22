const net = require('net');
const ws = require('ws');
const http = require('http');

const staticHandle = require('./static');

const tcpConnections = new Set();
const wsConnections = new Set();

const tcpServer = net.createServer(c => {
    console.log('TCP Client connected');

    c.on('end', () => {
        console.log('TCP Client disconnected');
        tcpConnections.delete(c);
    });

    c.on('data', data => {
        console.log(`Sending TCP data to ${wsConnections}`);
        for(const x of wsConnections) x.send(data);
    });

    tcpConnections.add(c);
});

tcpServer.on('error', (err) => { throw err; });

const httpServer = http.createServer();
httpServer.on("request", staticHandle(""));

const wsServer = new ws.Server({ server: httpServer });
wsServer.on('connection', c => {
    console.log("WS Client connected");

    c.on("pong", () => c.isAlive = true);

    c.on("message", message => {
        console.log(`Sending WS data to ${tcpConnections}`);
        for(const x of tcpConnections) x.write(message);
    });

    c.on('close', () => {
        console.log("WS Client disconnected");
        wsConnections.delete(c);
    });

    wsConnections.add(c);
});

console.log("Listening...");
tcpServer.listen(8081);
httpServer.listen(8080);
