const { createServer } = require('node:http');
const fs = require('fs');

const FILE = 'posts.json';

let posts = [];

try {
    const data = fs.readFileSync(FILE, 'utf-8');
    posts = JSON.parse(data);
} catch {
    posts = [];
}

function savePosts() {
    fs.writeFileSync(FILE, JSON.stringify(posts, null, 2));
}

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
        try {
            const post = JSON.parse(body);

            const ip = req.socket.remoteAddress;

            // 🔥 Count posts from this user
            const userPosts = posts.filter(p => p.ip === ip);

            if (userPosts.length >= 2) {
                res.statusCode = 403;
                res.setHeader('Content-Type', 'application/json');
                res.end(JSON.stringify({ error: "You already made 2 posts" }));
                return;
            }

            post.ip = ip;

            posts.push(post);
            savePosts();

            res.setHeader('Content-Type', 'application/json');
            res.end(JSON.stringify({ success: true }));

            } catch (err) {
                res.statusCode = 400;
                res.end(JSON.stringify({ error: 'Invalid JSON' }));
            }
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