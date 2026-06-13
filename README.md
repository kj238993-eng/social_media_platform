# VibeNet - Mini Social Media Platform

VibeNet is a modern, responsive full-stack social media application built using **Django** for the backend and database, and **Vanilla HTML, CSS, and JavaScript** for the frontend. 

It is designed with a premium, sleek dark-mode aesthetic featuring glassmorphism elements, responsive layouts, and smooth, responsive client-side interactions.

---

## ✨ Features

- **🔒 User Authentication**: Robust registration, login, and logout flow using Django's session authentication.
- **🖼️ Auto Avatars**: Generates unique, beautiful avatars for every registered user automatically using the Dicebear API.
- **📰 Dual Feeds**: Toggle between a **Global Feed** (all posts) and a **Following Feed** (posts only from creators you follow).
- **📝 Post Sharing**: Post thoughts with text and optional image URLs.
- **❤️ AJAX Likes**: Like or unlike posts instantly with visual bounce animations without reloading the page.
- **💬 AJAX Comments**: Instantly add comments to posts and view existing comments dynamically.
- **👤 Dynamic Profiles**: Custom profile pages displaying the user's posts, bio, statistics (posts, followers, following counts), and a follow/unfollow toggle.
- **📱 Responsive Layout**: Premium sidebar navigation that shifts into a sleek bottom navigation bar for mobile viewports.

---

## 🛠️ Tech Stack

- **Backend**: Python, Django (6.x)
- **Database**: SQLite (built-in, zero setup required)
- **Frontend**: HTML5, Vanilla CSS3 (Glassmorphism layout, modern typography), Vanilla JavaScript (AJAX Fetch API)

---

## 🚀 How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/kj238993-eng/social_media_platform.git
cd social_media_platform
```

### 2. Install Dependencies
Ensure you have Python installed. Then, install Django:
```bash
pip install django
```

### 3. Run Migrations
Set up your SQLite database tables:
```bash
python manage.py migrate
```

### 4. Run the Development Server
```bash
python manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your web browser. Register an account and start sharing your vibe!
