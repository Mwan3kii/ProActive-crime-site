function like(postId) {
  // Get references to the HTML elements displaying like count and the like button
  const likeCount = document.getElementById(`likes-count-${postId}`);
  const likeButton = document.getElementById(`like-button-${postId}`);

  // Send a POST request to the server endpoint for liking/unliking a post
  fetch(`/like-post/${postId}`, { method: "POST" })
    .then((res) => res.json()) // Parse the response as JSON
    .then((data) => {
      // Update the like count displayed on the page
      likeCount.innerHTML = data["likes"];

      // Update the like button icon based on whether the post is liked or not
      if (data["liked"] === true) {
        likeButton.className = "fas fa-star"; // Solid star icon (liked)
      } else {
        likeButton.className = "far fa-star"; // Outline star icon (not liked)
      }
    })
    .catch((e) => alert("Could not like post.")); // Display an alert if there's an error
}