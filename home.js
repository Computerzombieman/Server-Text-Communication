var objectList = document.getElementById('list');
const nameInput = document.getElementById('name');
const btn = document.getElementById('btn');

const API = "https://server-text-communication.onrender.com/posts";

function addPost(title, date, comments, description) {
    var newPost = document.createElement('li');

    newPost.className = "row";
    newPost.innerHTML = `
        <a class="attribute" href="./Thread.html">
            <h4 class="title">${title}</h4>
            <div class="bottom">
                <p class="timestamp">${date}</p>
                <p class="comment-count">${comments} comments</p>
            </div>
        </a>
    `;

    objectList.appendChild(newPost);
}

async function loadPosts() {
    try {
        const res = await fetch(API);
        const posts = await res.json();

        objectList.innerHTML = "";

        for (let post of posts) {
            addPost(
                post.title,
                post.date,
                post.comments,
                post.description
            );
        }
    } catch (err) {
        console.error("Failed to load posts:", err);
    }
}

btn.addEventListener('click', async function () {
    const nameValue = nameInput.value;

    if (nameValue.length > 0) {
        const newPost = {
            title: nameValue,
            date: new Date().toLocaleDateString(),
            comments: 0,
            description: "."
        };

        try {
            await fetch(API, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(newPost)
            });

            nameInput.value = '';
            loadPosts();
        } catch (err) {
            console.error("Failed to post:", err);
        }
    }
});

setInterval(loadPosts, 3000);

loadPosts();