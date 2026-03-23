# 🚀 Scalable Social Media Backend (Django + DRF + WebSockets)

A production-level social media backend system built using **Django REST Framework** and **Django Channels**, featuring real-time chat, notifications, and user presence — inspired by platforms like Instagram and WhatsApp.

---

## 🔥 Key Features

### 🔐 Authentication & Security

* JWT-based authentication (Login, Register, Logout)
* Secure password reset using token-based flow (`uidb64`, reset tokens)
* Environment-based configuration using `.env`

---

### 👥 Social Features

* Follow / Unfollow system
* Followers & Following APIs
* User profile management with media upload

---

### 📸 Post Management

* Create, update, delete posts
* Support for image/video uploads
* Multiple media handling
* Like / Unlike functionality
* Comment system

---

### 📰 Feed System

* Personalized feed (following + explore logic)
* Pagination for optimized performance

---

### 🔔 Real-Time Notifications

* Notifications for likes, comments, and follows
* Unread notification count
* Mark notifications as read
* Real-time delivery using WebSockets

---

### 💬 Real-Time Chat System

* One-to-one chat system
* Dynamic chat room creation (no duplicates)
* JWT authentication in WebSocket
* Real-time messaging using Django Channels
* Message persistence in database

---

### 🧠 Advanced Chat Features

* Chat inbox API (latest message per user)
* Unread message counter
* Message seen functionality

---

### 🟢 User Presence System

* Real-time Online / Offline status
* Last seen tracking
* Separate WebSocket consumer for stability

---

## ⚡ Tech Stack

* **Backend:** Django, Django REST Framework
* **Real-Time:** Django Channels, WebSockets
* **Database:** MySQL
* **Cache / Channel Layer:** Redis
* **Authentication:** JWT
* **Environment Management:** python-dotenv

---

## 🧠 Architecture Overview

* Modular app-based structure:

  * `accounts` → Authentication & user management
  * `posts` → Post & feed system
  * `interactions` → Likes, comments, chat
  * `notifications` → Notification system
  * `status` → Online/offline tracking

* Async handling using:

  * `database_sync_to_async`
  * Channel layers with Redis

---

## 🔄 Core Flow (Chat Example)

User sends message → WebSocket connection → Consumer receives →
Message saved in DB → Broadcast via group_send →
Receiver gets message in real-time

---

## 🛠️ Setup Instructions

```bash
# Clone repository
git clone https://github.com/deep1996feb/scalable-social-media-backend-project.git

cd scalable-social-media-backend-project

# Create virtual environment
python -m venv env
env\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```

---

## 🔐 Environment Variables

Create a `.env` file in the root directory:

```
DEBUG=True
SECRET_KEY=your_secret_key
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=3306
```

---

## 🚀 Future Improvements

* Dockerization for easy deployment
* Cloud deployment (AWS / Render)
* Redis-based caching for performance optimization
* Rate limiting & API throttling
* Group chat support

---

## 💡 Key Learnings

* Real-time communication using WebSockets
* Handling async operations in Django
* JWT authentication in WebSocket connections
* Scalable backend architecture design
* Debugging complex real-time systems

---

## 👨‍💻 Author

**Deepanshu Soni**
Backend Developer | Python | Django | Real-Time Systems

---

## ⭐ If you found this useful, consider giving a star!
