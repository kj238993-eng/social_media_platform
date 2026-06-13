// helper function to retrieve csrf token from cookies
function getCsrfToken() {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, 10) === 'csrftoken=') {
                cookieValue = decodeURIComponent(cookie.substring(10));
                break;
            }
        }
    }
    return cookieValue;
}

// toggle like status asynchronously
function likePost(postId) {
    const postCard = document.querySelector(`.post-card[data-post-id="${postId}"]`);
    if (!postCard) return;
    
    const likeBtn = postCard.querySelector('.like-btn');
    const likeCountSpan = likeBtn.querySelector('.like-count');
    const likeIcon = likeBtn.querySelector('i');
    
    const csrfToken = getCsrfToken();
    
    fetch(`/post/${postId}/like/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error("Like error response:", data.error);
            return;
        }
        
        likeCountSpan.textContent = data.likes_count;
        if (data.liked) {
            likeBtn.classList.add('liked');
            likeIcon.classList.remove('fa-regular');
            likeIcon.classList.add('fa-solid');
        } else {
            likeBtn.classList.remove('liked');
            likeIcon.classList.remove('fa-solid');
            likeIcon.classList.add('fa-regular');
        }
    })
    .catch(err => console.error("Like error:", err));
}

// toggle comments section visibility
function toggleComments(postId) {
    const commentsSection = document.getElementById(`comments-${postId}`);
    if (!commentsSection) return;
    
    if (commentsSection.style.display === 'none') {
        commentsSection.style.display = 'block';
    } else {
        commentsSection.style.display = 'none';
    }
}

// submit comment asynchronously
function submitComment(event, postId) {
    event.preventDefault();
    
    const inputElement = document.getElementById(`comment-input-${postId}`);
    const content = inputElement.value.trim();
    if (!content) return;
    
    const csrfToken = getCsrfToken();
    
    fetch(`/post/${postId}/comment/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ content: content })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }
        
        // Clear input
        inputElement.value = '';
        
        // Remove "No comments" placeholder if it exists
        const noCommentsText = document.getElementById(`no-comments-${postId}`);
        if (noCommentsText) {
            noCommentsText.remove();
        }
        
        // Add comment to DOM
        const commentsList = document.getElementById(`comments-list-${postId}`);
        const commentItem = document.createElement('div');
        commentItem.className = 'comment-item';
        commentItem.innerHTML = `
            <img src="${data.profile_picture_url || 'https://api.dicebear.com/7.x/avataaars/svg?seed=' + data.username}" alt="avatar" class="avatar-sm">
            <div class="comment-content-box">
                <div class="comment-header">
                    <span class="comment-author">@${data.username}</span>
                    <span class="comment-time">${data.created_at}</span>
                </div>
                <p class="comment-text">${escapeHtml(data.content)}</p>
            </div>
        `;
        
        commentsList.appendChild(commentItem);
        commentsList.scrollTop = commentsList.scrollHeight;
        
        // Update comments count in footer
        const postCard = document.querySelector(`.post-card[data-post-id="${postId}"]`);
        if (postCard) {
            const commentToggleBtn = postCard.querySelector('.comment-toggle-btn span');
            if (commentToggleBtn) {
                const currentCount = parseInt(commentToggleBtn.textContent, 10) || 0;
                commentToggleBtn.textContent = currentCount + 1;
            }
        }
    })
    .catch(err => console.error("Comment submission error:", err));
}

// follow/unfollow users from suggestions panel
function toggleFollow(button, userId) {
    const csrfToken = getCsrfToken();
    
    fetch(`/user/${userId}/follow/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }
        
        if (data.following) {
            button.textContent = 'Unfollow';
            button.classList.remove('btn-primary');
            button.classList.add('btn-secondary');
        } else {
            button.textContent = 'Follow';
            button.classList.remove('btn-secondary');
            button.classList.add('btn-primary');
        }
    })
    .catch(err => console.error("Follow error:", err));
}

// utility to escape user inputs to prevent XSS
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, function(m) { return map[m]; });
}
