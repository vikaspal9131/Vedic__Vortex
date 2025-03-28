import { initializeApp } from "https://www.gstatic.com/firebasejs/11.4.0/firebase-app.js";
import { getAuth, signInWithPopup, GoogleAuthProvider } from "https://www.gstatic.com/firebasejs/11.4.0/firebase-auth.js";

// Firebase config
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
const provider = new GoogleAuthProvider();

// Google Sign-In
document.getElementById("google-btn").addEventListener("click", async () => {
    try {
        const result = await signInWithPopup(auth, provider);
        const user = result.user;
        
        // Store user info in localStorage
        localStorage.setItem("userPhoto", user.photoURL);
        localStorage.setItem("userName", user.displayName);

        // Redirect to index.html
        window.location.href = "/src/index.html";
    } catch (error) {
        console.error("Login Error:", error.message);
    }
});
