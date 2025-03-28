
window.addEventListener('load', function () {
  const loaderTimeout = 1500; 
  setTimeout(() => {
      document.getElementById('loader').style.display = 'none';
      content.style.display = 'block'; 
  }, loaderTimeout);
});


const locoScroll = new LocomotiveScroll({
  el: document.querySelector("#main"),
  smooth: true ,
  lerp:0.07
});




document.addEventListener("DOMContentLoaded", () => {
  const userImg = document.getElementById("user-img");
  const loginBtn = document.getElementById("login-btn");
  const userProfile = document.getElementById("user-profile");

  // Get user data from localStorage
  const userPhoto = localStorage.getItem("userPhoto");

  if (userPhoto) {
      userImg.src = userPhoto;
      userProfile.style.display = "block"; // Show profile section
      loginBtn.style.display = "none"; // Hide login button
  } else {
      userProfile.style.display = "none"; // Hide profile section
      loginBtn.style.display = "inline-block"; // Show login button
  }
});
