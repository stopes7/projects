document.addEventListener("DOMContentLoaded", function() {
  const likeBtn = document.getElementById("like-btn");
  const dislikeBtn = document.getElementById("dislike-btn");

  function ajaxPost(url, success) {
    fetch(url, {
      method: "POST",
      headers: {
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: "{}"
    }).then(r => r.json()).then(success).catch(e => console.error(e));
  }

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + "=")) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  if (likeBtn) {
    likeBtn.addEventListener("click", function() {
      const id = this.dataset.id;
      ajaxPost(`/like/${id}/`, function(data) {
        document.getElementById("likes").innerText = data.likes;
      });
    });
  }

  if (dislikeBtn) {
    dislikeBtn.addEventListener("click", function() {
      const id = this.dataset.id;
      ajaxPost(`/dislike/${id}/`, function(data) {
        document.getElementById("dislikes").innerText = data.dislikes;
      });
    });
  }
});
