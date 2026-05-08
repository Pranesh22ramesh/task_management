# Smart Task Management System (Full-Stack)

A professional, production-grade Task Management System built with Python Flask, PostgreSQL, and modern web technologies. This project features real-time updates via WebSockets, advanced analytics with Pandas/NumPy, and a sleek, responsive UI.

## 🚀 Features

- **Robust Authentication**: Secure registration and login with session management and password hashing (Werkzeug).
- **Task Management (CRUD)**: Full suite of task operations with priority levels, status tracking, and due dates.
- **Real-time Synchronization**: Instant UI updates and notifications powered by **Flask-SocketIO**.
- **Data Analytics**: Insightful statistics and trends calculated using **Pandas** and **NumPy**.
- **Data Export**: Export your tasks directly to a CSV file.
- **Modern UI/UX**: Professional "Blue + Black" theme, dark mode support, and smooth animations using Bootstrap 5 and custom CSS.
- **Responsive Design**: Mobile-friendly layout with a collapsible sidebar.
- **Interactive Charts**: Dynamic data visualization using **Chart.js**.

## 🛠️ Tech Stack

- **Backend**: Python, Flask, Flask-SQLAlchemy, Flask-Login, Flask-SocketIO
- **Database**: PostgreSQL
- **Data Processing**: Pandas, NumPy
- **Frontend**: HTML5, CSS3 (Bootstrap 5), JavaScript (Vanilla), Socket.IO Client, Chart.js
- **Utilities**: PyJWT, Flask-Migrate, Python-Dotenv

## 📦 Installation & Setup

### 1. Prerequisites
- Python 3.9+
- PostgreSQL
- Node.js (Optional, for advanced frontend tooling)

### 2. Clone and Install
```bash
git clone <repository-url>
cd smart-task-manager
pip install -r requirements.txt
```

### 3. Database Configuration
1. Create a PostgreSQL database: `CREATE DATABASE smart_task_db;`.
2. Create a `.env` file in the root directory:
```env
SECRET_KEY=your_secret_key_here
DATABASE_URL=postgresql://username:password@localhost:5432/smart_task_db
```

### 4. Initialize Database
```python
from app import app, db
with app.app_context():
    db.create_all()
```

### 5. Run the Application
```bash
python app.py
```
Visit `http://localhost:5000` to start managing your tasks!

## 📊 Analytics & WebSockets

### Analytics Logic
The system fetches raw task data from PostgreSQL and processes it into a **Pandas DataFrame**. **NumPy** is then used for high-performance calculations of completion rates, priority distribution, and trends.

### WebSocket Implementation
We use a dedicated service to broadcast events (`task_added`, `task_updated`, `task_deleted`) across all connected clients. This ensures that if you add a task on one device, it appears instantly on others without a page refresh.

## 📄 API Documentation

- `POST /register`: User registration.
- `POST /login`: User authentication.
- `GET /api/tasks`: Fetch all tasks for current user.
- `POST /api/tasks`: Create a new task.
- `PUT /api/tasks/<id>`: Update an existing task.
- `DELETE /api/tasks/<id>`: Remove a task.
- `GET /api/analytics`: Fetch pre-calculated productivity stats.
- `GET /api/tasks/export`: Download tasks as CSV.

## 🎨 UI Preview
- **Professional Dashboard**: Clean tables and rounded cards.
- **Dark Mode**: Seamless theme switching for better accessibility.
- **Live Notifications**: Non-intrusive toast messages for real-time updates.

---
Developed as an interview-ready full-stack showcase.
