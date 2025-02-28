document.addEventListener('DOMContentLoaded', function () {
    // Funkcija obrabotki lajkow i dizlajkow
    document.querySelectorAll('.post').forEach(post => {
        const likeBtn = post.querySelector('.like-btn');
        const dislikeBtn = post.querySelector('.dislike-btn');

        likeBtn.addEventListener('click', function () {
            sendReaction(post.dataset.postId, 'like');
        });

        dislikeBtn.addEventListener('click', function () {
            sendReaction(post.dataset.postId, 'dislike');
        });
    });

    // Funkcija zagruzki kommentariew czerez ajax
    document.querySelectorAll('.post').forEach(post => {
        loadComments(post.dataset.postId, post.querySelector('.comments'));
    });
});

// Otprawka lajkow i dizlajkow na server
function sendReaction(postId, reaction) {
    fetch(`/post/${postId}/${reaction}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'  // Ukazywaem czto otprawlaem json
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Ошибка HTTP: ${response.status}`); // Еesli oszibka 
        }
        return response.json(); // Peredelywaem w json
    })
    .then(data => {
        console.log(`Реакция: ${reaction} на пост ${postId}`, data);
    })
    .catch(error => console.error('Oszibka otprawki reakcii:', error));
}

// Zagruzka kommentariew
function loadComments(postId, commentContainer) {
    fetch(`/post/${postId}/comments`)
        .then(response => response.json())
        .then(comments => {
            commentContainer.innerHTML = '';
            comments.forEach(comment => {
                const commentElement = document.createElement('p');
                commentElement.textContent = comment.content;
                commentContainer.appendChild(commentElement);
            });
        })
        .catch(error => console.error('Oszibka zagruzki kommentariew:', error));
}
