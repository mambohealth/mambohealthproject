document.addEventListener('DOMContentLoaded', function() {
  // Inline edit
  document.querySelectorAll('.inline-edit').forEach(function(input) {
    input.addEventListener('change', function() {
      const pk = this.dataset.pk;
      const field = this.dataset.field;
      const value = this.value;
      fetch(`/health/ajax/record/${pk}/update/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': getCookie('csrftoken'),
        },
        body: `field=${field}&value=${encodeURIComponent(value)}`
      })
      .then(r => r.json())
      .then(data => {
        if (!data.success) alert('Update failed: ' + (data.error || 'Unknown error'));
      });
    });
  });

  // Comments toggle
  document.querySelectorAll('.comment-btn').forEach(function(btn) {
    btn.addEventListener('click', function() {
      const pk = this.dataset.pk;
      const row = document.getElementById('comments-' + pk);
      if (row.style.display === 'none') {
        row.style.display = '';
        loadComments(pk, row.querySelector('.comments-list'));
      } else {
        row.style.display = 'none';
      }
    });
  });

  // Comment form submit (event delegation)
  document.querySelectorAll('.comment-form').forEach(function(form) {
    form.addEventListener('submit', function(e) {
      e.preventDefault();
      const pk = this.dataset.pk;
      const input = this.querySelector('input[name="comment"]');
      fetch(`/health/ajax/record/${pk}/comment/add/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': getCookie('csrftoken'),
        },
        body: `comment=${encodeURIComponent(input.value)}`
      })
      .then(r => r.json())
      .then(data => {
        if (data.success) {
          input.value = '';
          loadComments(pk, this.closest('.comment-row').querySelector('.comments-list'));
        } else {
          alert('Comment failed: ' + (data.error || 'Unknown error'));
        }
      }.bind(this));
    });
  });

  function loadComments(pk, container) {
    fetch(`/health/ajax/record/${pk}/comments/`)
      .then(r => r.json())
      .then(data => {
        container.innerHTML = '';
        if (data.comments.length === 0) {
          container.innerHTML = '<div class="text-gray-400">No comments yet.</div>';
        } else {
          data.comments.forEach(function(c) {
            const div = document.createElement('div');
            div.className = 'mb-1';
            div.innerHTML = `<span class='font-bold'>${c.user}</span> <span class='text-xs text-gray-500'>${c.created_at}</span>: ${c.comment}`;
            container.appendChild(div);
          });
        }
      });
  }

  // CSRF helper
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
});
