const { createServer } = require('node:http');

let posts = [];

const server = createServer((req, res) => {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    if (req.method === 'OPTIONS') {
        res.writeHead(204);
        res.end();
        return;
    }

    if (req.method === 'GET' && req.url === '/posts') {
        res.setHeader('Content-Type', 'application/json');
        res.end(JSON.stringify(posts));
        return;
    }

    if (req.method === 'POST' && req.url === '/posts') {
        let body = '';

        req.on('data', chunk => body += chunk);

        req.on('end', () => {
            const post = JSON.parse(body);
            posts.push(post);

            res.setHeader('Content-Type', 'application/json');
            res.end(JSON.stringify({ success: true }));
        });

        return;
    }

    res.statusCode = 404;
    res.end('Not found');
});

const PORT = process.env.PORT || 3000;

server.listen(PORT, () => {
    console.log('Server running on port ' + PORT);
});