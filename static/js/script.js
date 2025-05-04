document.addEventListener('DOMContentLoaded', function() {
    // Like button functionality
    document.querySelectorAll('.like-button').forEach(button => {
        button.addEventListener('click', async function() {
            const postId = this.dataset.postId;
            const postType = this.dataset.postType;
            const likeCount = this.querySelector('.like-count');
            
            try {
                const response = await fetch(`/${postType}s/${postId}/like/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                        'Content-Type': 'application/json'
                    }
                });
                
                const data = await response.json();
                if (data.success) {
                    // Update like count
                    likeCount.textContent = data.likes_count;
                    
                    // Add animation class
                    this.classList.add('like-animation');
                    setTimeout(() => {
                        this.classList.remove('like-animation');
                    }, 300);
                    
                    // Update button color
                    if (data.liked) {
                        this.classList.add('text-red-500');
                    } else {
                        this.classList.remove('text-red-500');
                    }
                }
            } catch (error) {
                console.error('Error:', error);
            }
        });
    });

    // Comment button functionality
    document.querySelectorAll('.comment-button').forEach(button => {
        button.addEventListener('click', function() {
            const commentsSection = this.closest('.bg-white').querySelector('.comments-section');
            commentsSection.classList.toggle('hidden');
        });
    });

    // Comment form submission
    document.querySelectorAll('.comments-section form').forEach(form => {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            const input = this.querySelector('input');
            const postId = this.closest('.bg-white').querySelector('.like-button').dataset.postId;
            const postType = this.closest('.bg-white').querySelector('.like-button').dataset.postType;
            
            if (input.value.trim()) {
                try {
                    const response = await fetch(`/${postType}s/${postId}/comment/`, {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': getCookie('csrftoken'),
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            content: input.value.trim()
                        })
                    });
                    
                    const data = await response.json();
                    if (data.success) {
                        // Add new comment to the list
                        const commentsList = this.previousElementSibling;
                        const newComment = document.createElement('div');
                        newComment.className = 'flex items-start space-x-2';
                        newComment.innerHTML = `
                            <img src="/static/images/default-avatar.png" alt="${data.comment.user}" class="w-8 h-8 rounded-full">
                            <div>
                                <p class="font-medium">${data.comment.user}</p>
                                <p class="text-gray-600">${data.comment.content}</p>
                            </div>
                        `;
                        commentsList.appendChild(newComment);
                        
                        // Clear input
                        input.value = '';
                    }
                } catch (error) {
                    console.error('Error:', error);
                }
            }
        });
    });

    // Gift button functionality
    document.querySelectorAll('.gift-button').forEach(button => {
        button.addEventListener('click', function() {
            const postId = this.closest('.bg-white').querySelector('.like-button').dataset.postId;
            const postType = this.closest('.bg-white').querySelector('.like-button').dataset.postType;
            window.location.href = `/${postType}s/${postId}/gift/`;
        });
    });

    // Helper function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Infinite scroll functionality
    let loading = false;
    let page = 1;
    const feed = document.querySelector('.space-y-6');

    window.addEventListener('scroll', async function() {
        if (loading) return;
        
        if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 1000) {
            loading = true;
            page++;
            
            try {
                const response = await fetch(`/?page=${page}`);
                const html = await response.text();
                
                if (html) {
                    const temp = document.createElement('div');
                    temp.innerHTML = html;
                    const newPosts = temp.querySelector('.space-y-6').children;
                    
                    Array.from(newPosts).forEach(post => {
                        feed.appendChild(post);
                    });
                }
            } catch (error) {
                console.error('Error:', error);
            }
            
            loading = false;
        }
    });
}); 