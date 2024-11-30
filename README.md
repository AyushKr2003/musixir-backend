# Musixir Backend

A high-performance FastAPI backend server for the Musixir music streaming application, built with Python and SQLAlchemy.

## 🚀 Features

- 🔐 User Authentication & Authorization
- 🎵 Music File Management
- 🔍 Search Functionality
- 🎧 Favorite Songs Management
- 💾 Cloud File Storage
- ⚡ High-Performance API

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **Database**: SQLAlchemy with PostgreSQL
- **File Storage**: Cloudinary
- **Authentication**: JWT with bcrypt
- **API Documentation**: Swagger UI (built-in with FastAPI)
- **Environment**: Python-dotenv

## 📋 Prerequisites

- Python 3.8 or higher
- PostgreSQL
- pip (Python package manager)
- Cloudinary account

## 🔧 Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd server
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Unix/MacOS
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables in `.env`:
```env
# Database Configuration
DB_USER=postgres          # Your PostgreSQL username
DB_PASSWORD=your_password # Your PostgreSQL password
DB_HOST=localhost        # Database host (default: localhost)
DB_PORT=5432            # PostgreSQL port (default: 5432)
DB_NAME=musicapp        # Your database name

# Cloudinary Configuration
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# Security
PASSWORD_KEY=your_secure_password_key
```

These environment variables are used in `database.py` to construct the PostgreSQL connection URL:
```python
# Get database credentials from environment variables
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "musicapp")

# Construct database URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
```

5. Start the server:
```bash
# Development
uvicorn main:app --reload

# Production
uvicorn main:app
```

## 📁 Project Structure

```
server/
├── routes/                 # API route handlers
│   ├── auth.py             # Authentication routes
│   └── song.py             # Music management
├── models/                 # SQLAlchemy models
│   ├── base.py             # Base model configuration
│   ├── song.py             # Song model
│   └── user.py             # User model
├── middleware/             # Custom middleware
├── pydantic_schema/        # Request/Response schemas
├── database.py             # Database configuration
├── main.py                 # App entry point
└── requirements.txt        # Python dependencies
```

## 🔌 API Endpoints

### Authentication
- `POST /auth/signup` - Register new user
- `POST /auth/login` - User login
- `GET /auth/` - Get current user

### Music
- `GET /song/list` - Get all songs
- `POST /song/upload` - Upload new song
- `POST /song/favorite` - Add to favorites
- `DELETE /song/favorites` - Remove from favorites

## 🔒 Security

- Password hashing using bcrypt
- CORS configuration
- Secure HTTP headers
- Request validation with Pydantic

## 📚 Documentation

API documentation is automatically generated and available at:
- Swagger UI: `/docs`
- ReDoc: `/redoc`

## 📝 License

This project is licensed under the [MIT License](LICENSE) - see the [LICENSE](LICENSE) file for details.

## 🤝 Acknowledgments

- FastAPI team
- SQLAlchemy team
- Cloudinary
- All contributors

---

Made with ❤️ for Musixir Music App
