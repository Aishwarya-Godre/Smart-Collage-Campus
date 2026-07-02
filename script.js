// ============================================
//  Smart Campus App - Frontend Script
// ============================================

const API_BASE_URL = 'http://localhost:3000/api';

/* =========================
   START BUTTON (HOME)
========================= */
const startBtn = document.getElementById("startBtn");
if (startBtn) {
    startBtn.onclick = function () {
        alert("Welcome to Campus Guru!");
    };
}

/* =========================
   BACK BUTTON
========================= */
function goBack() {
    window.history.back();
}

/* =========================
   SIGNUP VALIDATION (WITH BACKEND)
========================= */
async function createAccount() {
    const name = document.querySelector('input[type="text"]').value.trim();
    const email = document.querySelector('input[type="email"]').value.trim();
    const password = document.querySelector('input[type="password"]').value.trim();

    if (!name || !email || !password) {
        alert("⚠️ Please fill all details!");
        return;
    }

    if (!email.includes("@")) {
        alert("⚠️ Enter valid email!");
        return;
    }

    if (password.length < 6) {
        alert("⚠️ Password must be at least 6 characters!");
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, password })
        });

        const data = await response.json();

        if (response.ok) {
            alert("✅ Account Created Successfully!");
            window.location.href = "signIn.html";
        } else {
            alert("❌ Registration failed: " + (data.error || "Unknown error"));
        }
    } catch (err) {
        console.error('Signup error:', err);
        alert("❌ Cannot connect to backend server. Is it running?");
    }
}

/* =========================
   PROFILE IMAGE UPLOAD
========================= */
const imageInput = document.getElementById("imageInput");
const profileImage = document.getElementById("profileImage");

window.onload = function () {
    let savedImage = localStorage.getItem("profileImage");
    if (savedImage && profileImage) {
        profileImage.src = savedImage;
    }
};

if (imageInput) {
    imageInput.addEventListener("change", function () {
        const file = this.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                if (profileImage) {
                    profileImage.src = e.target.result;
                }
                localStorage.setItem("profileImage", e.target.result);
            };
            reader.readAsDataURL(file);
        }
    });
}

/* =========================
   LOGIN (WITH BACKEND)
========================= */
const loginForm = document.getElementById("loginForm");
if (loginForm) {
    loginForm.addEventListener("submit", async function (e) {
        e.preventDefault(); // stop page reload

        const email = document.getElementById("loginEmail").value.trim();
        const password = document.getElementById("loginPassword").value.trim();

        if (!email || !password) {
            alert("⚠️ Please fill all details!");
            return;
        }

        try {
            const response = await fetch(`${API_BASE_URL}/auth/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if (response.ok) {
                alert("✅ Login Successful!");
                localStorage.setItem("userLoggedIn", "true");
                localStorage.setItem("userName", data.user.name);
                localStorage.setItem("userEmail", data.user.email);
                window.location.href = "dashboard.html";
            } else {
                alert("❌ " + (data.error || "Invalid email or password!"));
            }
        } catch (err) {
            console.error('Login error:', err);
            alert("❌ Cannot connect to backend server. Is it running?");
        }
    });
}

/* =========================
   PASSWORD TOGGLE
========================= */
function togglePassword(id) {
    const input = document.getElementById(id);
    if (input) {
        input.type = input.type === "password" ? "text" : "password";
    }
}

/* =========================
   BOTTOM NAV / TABS & UTILS
========================= */
const tabs = document.querySelectorAll(".tab");
tabs.forEach(tab => {
    tab.addEventListener("click", () => {
        tabs.forEach(t => t.classList.remove("active"));
        tab.classList.add("active");
    });
});

const eventsBtn = document.getElementById("eventsBtn");
const latestBtn = document.getElementById("latestBtn");
const clubsBtn = document.getElementById("clubsBtn");
const addPostBtn = document.getElementById("addPostBtn");

if (eventsBtn)  eventsBtn.onclick = () => window.location.href = 'upcoming.html';
if (latestBtn)  latestBtn.onclick = () => window.location.href = 'Latest.html';
if (clubsBtn)   clubsBtn.onclick = () => window.location.href = 'clubs.html';
if (addPostBtn) addPostBtn.onclick = () => window.location.href = 'addPost.html';

const navItems = document.querySelectorAll(".nav-item");
navItems.forEach((item, index) => {
    item.addEventListener("click", () => {
        navItems.forEach(nav => nav.classList.remove("active"));
        item.classList.add("active");

        if (index === 0) window.location.href = 'dashboard.html';
        else if (index === 1) window.location.href = 'upcoming.html';
        else if (index === 2) window.location.href = 'addPost.html';
        else if (index === 3) window.location.href = 'clubs.html';
        else if (index === 4) window.location.href = 'profile.html';
    });
});

function setActive(element) {
    const items = document.querySelectorAll(".nav-item");
    items.forEach(item => item.classList.remove("active"));
    element.classList.add("active");
}

function logout() {
    const confirmLogout = confirm("Are you sure you want to logout?");
    if (confirmLogout) {
        localStorage.removeItem("userLoggedIn");
        localStorage.removeItem("userName");
        localStorage.removeItem("userEmail");
        window.location.href = "signIn.html";
    }
}