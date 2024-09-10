document.addEventListener('DOMContentLoaded', function() {
    const likeForm = document.getElementById('like-form');
    const likeButton = document.getElementById('like-button');
    const likesCountElement = document.getElementById('likes-count');

    likeForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission

        const formData = new FormData(likeForm);
        const url = likeForm.action;

        fetch(url, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.likes_count !== undefined) {
                likesCountElement.textContent = `Likes: ${data.likes_count}`;
                likeButton.textContent = data.liked ? 'Unlike' : 'Like';
            } else {
                console.error('Error updating likes count:', data.error);
            }
        })
        .catch(error => console.error('Error:', error));
    });
});