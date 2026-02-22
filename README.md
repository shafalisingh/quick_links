# QuickLink - URL Shortener

A full-stack URL shortening service with click analytics, built with FastAPI, PostgreSQL, and Docker.

![QuickLink Demo](https://img.shields.io/badge/status-active-success.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)
![Docker](https://img.shields.io/badge/Docker-ready-blue.svg)

## 🚀 Features

- **URL Shortening**: Convert long URLs into short, shareable links using base36 encoding
- **Click Analytics**: Track total clicks, timestamps, and click history for each shortened URL
- **Persistent Storage**: PostgreSQL database ensures data survives restarts
- **Modern UI**: Clean, responsive frontend with gradient design
- **Dockerized**: Fully containerized application for easy deployment
- **RESTful API**: Well-documented API endpoints with automatic Swagger docs

## 🛠️ Tech Stack

**Backend:**
- FastAPI (Python web framework)
- PostgreSQL (Relational database)
- asyncpg (Async PostgreSQL driver)
- Uvicorn (ASGI server)

**Frontend:**
- HTML5, CSS3, Vanilla JavaScript
- Responsive design
- Gradient UI with modern aesthetics

**DevOps:**
- Docker & Docker Compose
- Multi-container architecture
- Environment-based configuration

## 📊 Architecture
```
┌─────────────────────────────────────────────────┐
│           Docker Compose Network                │
│                                                 │
│  ┌──────────────┐         ┌─────────────────┐  │
│  │   FastAPI    │────────▶│   PostgreSQL    │  │
│  │  Container   │         │    Container    │  │
│  │              │         │                 │  │
│  │ - Python 3.11│         │ - Database      │  │
│  │ - API Logic  │         │ - Tables        │  │
│  │ - Frontend   │         │ - Analytics     │  │
│  │ - Port 8000  │         │ - Port 5432     │  │
│  └──────────────┘         └─────────────────┘  │
└─────────────────────────────────────────────────┘
```

## 🗄️ Database Schema

**urls table:**
```sql
id              SERIAL PRIMARY KEY
long_url        TEXT NOT NULL
created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

**clicks table:**
```sql
id              SERIAL PRIMARY KEY
url_id          INTEGER REFERENCES urls(id)
clicked_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
ip_address      VARCHAR(45)
user_agent      TEXT
```

## 🔧 Installation & Setup

### Prerequisites
- Docker Desktop
- Git

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/quicklink.git
cd quicklink
```

2. **Start the application**
```bash
docker-compose up --build
```

3. **Access the application**
- Frontend: http://localhost:8000/app
- API Docs: http://localhost:8000/docs

That's it! Docker handles all dependencies and setup.

## 📡 API Endpoints

### Shorten URL
```http
POST /shorten
Content-Type: application/json

{
  "long_url": "https://example.com/very-long-url"
}

Response:
{
  "short_code": "abc",
  "short_url": "http://localhost:8000/abc",
  "original_url": "https://example.com/very-long-url"
}
```

### Redirect to Original URL
```http
GET /{short_code}

Redirects to the original URL
```

### Get Analytics
```http
GET /analytics/{short_code}

Response:
{
  "short_code": "abc",
  "long_url": "https://example.com/very-long-url",
  "created_at": "2026-02-21T17:00:00",
  "total_clicks": 42,
  "recent_clicks": [...]
}
```

## 💡 Key Technical Implementations

### Base36 Encoding
- Converts numeric IDs to short alphanumeric codes (0-9, a-z)
- Example: ID 1000 → "rs"
- Provides 2.1 billion possible URLs with 6 characters

### Async Operations
- Non-blocking database queries using asyncpg
- Efficient handling of concurrent requests
- FastAPI's native async support

### Click Tracking
- Separate clicks table for granular analytics
- Indexed by url_id for fast lookups
- Tracks timestamp, IP, and user agent

### Docker Multi-Container Setup
- Isolated services for web and database
- Persistent volumes for data
- Health checks for startup dependencies
- Environment-based configuration

## 🎨 Frontend Features

- Real-time URL shortening
- One-click copy to clipboard
- Inline analytics viewing
- Responsive design for mobile/desktop
- Error handling and validation

## 🚀 Deployment

The application is production-ready and can be deployed to:
- AWS (ECS, EC2, or Fargate)
- Heroku (Container Registry)
- DigitalOcean (App Platform)
- Any Docker-compatible platform

## 📈 Future Enhancements

- [ ] Custom short codes (user-defined)
- [ ] QR code generation
- [ ] Link expiration dates
- [ ] User authentication
- [ ] Dashboard with charts
- [ ] Rate limiting per IP
- [ ] Redis caching layer
- [ ] Geographic analytics

## 🧪 Development

### Local Development (without Docker)
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Start PostgreSQL
# Create database: createdb quick_links

# Run the app
uvicorn main:app --reload
```

### Project Structure
```
quicklink/
├── main.py                 # FastAPI application
├── models.py               # Pydantic models
├── database.py             # Database operations
├── utils.py                # Helper functions (base36)
├── static/                 # Frontend files
│   ├── index.html
│   ├── style.css
│   └── script.js
├── Dockerfile              # Container definition
├── docker-compose.yml      # Multi-container orchestration
├── init.sql                # Database schema
└── requirements.txt        # Python dependencies
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


## 👨‍💻 Author

**Your Name**
- LinkedIn: [Your LinkedIn](https://www.linkedin.com/in/shafali-singh/)
- GitHub: [@yourusername](https://github.com/shafalisingh)

## 🙏 Acknowledgments

- Built as a learning project to master full-stack development
- Demonstrates proficiency in Python, FastAPI, PostgreSQL, Docker, and frontend development

---

**⭐ Star this repo if you found it helpful!**
