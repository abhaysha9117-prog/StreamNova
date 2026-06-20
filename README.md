# 🎬 StreamNova

StreamNova is a modern movie and TV streaming platform built with **Next.js** and **FastAPI**. It provides movie discovery, streaming, watch history, favorites management, extension support, and HLS video playback through a clean and responsive interface.

## 🚀 Live Demo

Frontend: https://stream-nova-steel.vercel.app

Backend API: https://streamnova-qgog.onrender.com

## ✨ Features

* 🎥 Movie & TV Series Streaming
* 🔍 Search Movies and Series
* ❤️ Favorites Management
* 📺 Watch History Tracking
* 🎞️ HLS Video Playback
* 🔌 Extension/Plugin System
* 📱 Responsive UI
* ⚡ FastAPI Backend
* ⚛️ Next.js Frontend
* 🗄️ SQLite Database
* 🌐 Cloud Deployment (Vercel + Render)

## 🛠️ Tech Stack

### Frontend

* Next.js 16
* React
* TypeScript
* Tailwind CSS
* HLS.js

### Backend

* FastAPI
* Python
* SQLAlchemy
* SQLite
* JWT Authentication
* Plugin Architecture

## 📂 Project Structure

```text
StreamNova/
│
├── frontend/
│   ├── app/
│   ├── components/
│   ├── public/
│   └── package.json
│
├── backend/
│   ├── auth/
│   ├── database/
│   ├── routers/
│   ├── plugins/
│   ├── extensions/
│   ├── repositories/
│   ├── main.py
│   └── requirements.txt
│
└── README.md
```

## ⚙️ Local Installation

### Clone Repository

```bash
git clone https://github.com/abhaysha9117-prog/StreamNova.git
cd StreamNova
```

### Backend Setup

```bash
cd backend

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

uvicorn main:app --reload
```

Backend will run at:

```text
http://localhost:8000
```

### Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Frontend will run at:

```text
http://localhost:3000
```

## 🌐 Deployment

### Frontend

Deployed on Vercel:

```text
https://stream-nova-steel.vercel.app
```

### Backend

Deployed on Render:

```text
https://streamnova-qgog.onrender.com
```

## 📌 API Endpoints

### Search

```http
GET /search?q=movie_name
```

### Movie Details

```http
GET /movie/{imdbID}
```

### Stream Sources

```http
GET /watch/streams/{imdbID}
```

### Favorites

```http
GET /favorites/list
POST /favorites/add
```

### Watch History

```http
GET /watch/list
POST /watch/save
```

## 🔮 Future Improvements

* User Authentication System
* Multiple Streaming Providers
* Advanced Search Filters
* Recommendation Engine
* Subtitle Management
* User Profiles
* Dark/Light Theme
* Cloud Storage Integration
* AI-powered Content Suggestions

## 👨‍💻 Author

**Abhay Kumar Sharma**

* GitHub: https://github.com/abhaysha9117-prog
* LinkedIn: [www.linkedin.com/in/abhay-kumar-sharma-047298265](http://www.linkedin.com/in/abhay-kumar-sharma-047298265)

## 📄 License

This project is intended for educational and learning purposes.

---

⭐ If you like this project, consider giving it a star on GitHub.
