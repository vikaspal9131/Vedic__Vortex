import { getAuth, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/11.0.1/firebase-auth.js";

const auth = getAuth();

document.addEventListener("DOMContentLoaded", () => {
  onAuthStateChanged(auth, (user) => {
    const getStartedBtn = document.querySelector('.sign-in-btn');
    const userProfile = document.querySelector('.user-profile');
    const userPhoto = document.getElementById("userPhoto");

    if (user) {
     
      const profilePhoto = user.photoURL;

      userPhoto.src = profilePhoto;
      userPhoto.alt = `${user.displayName}'s profile picture`;

     
      if (getStartedBtn) {
        getStartedBtn.style.display = 'none';
      }

     
      userProfile.style.display = 'block';
    } else {
     
      if (getStartedBtn) {
        getStartedBtn.style.display = 'inline-block';
      }
      
     
      userProfile.style.display = 'none';
    }
  });
});