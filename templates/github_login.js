import { initializeApp } from "https://www.gstatic.com/firebasejs/11.4.0/firebase-app.js";
import { getAuth, signInWithPopup, GithubAuthProvider, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/11.4.0/firebase-auth.js";

// Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyBnrOLlosTDGHCxXKZdFrO_ev-Oy2Ruv3U",
    authDomain: "nexora-213e2.firebaseapp.com",
    projectId: "nexora-213e2",
    storageBucket: "nexora-213e2.appspot.com",
    messagingSenderId: "998457123271",
    appId: "1:998457123271:web:436292c777f2d2b29b39e2",
    measurementId: "G-V74NX09TNP"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const provider = new GithubAuthProvider();  // ✅ Corrected for GitHub

// GitHub Login Button
const githubBtn = document.querySelector('#github-btn');

githubBtn.addEventListener("click", async () => {
    try {
        const result = await signInWithPopup(auth, provider);
        console.log("User signed in with GitHub:", result.user);
        window.location.href = "/frontend/dashboard.html";  // Redirect after login
    } catch (error) {
        console.error("GitHub Login Error:", error.message);
    }
});

// Check user login state
onAuthStateChanged(auth, (user) => {
    if (user) {
        console.log("User logged in:", user);
    } else {
        console.log("No user is signed in.");
    }
});




