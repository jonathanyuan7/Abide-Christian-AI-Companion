# Abide: Christian AI Companion

A gentle, privacy-respecting Christian app where users can share how they're feeling and receive relevant Bible verses, reflections, and prayers. The app also offers a 10-minute devotion generator with embedded YouTube content.

## Features

- **Feeling Response**: Share your feelings and get relevant Bible verses, pastoral reflection, and prayer
- **10-Minute Devotion Generator**: Structured devotion plans with scripture, reflection, and action steps
- **YouTube Integration**: Relevant worship songs and devotional content
- **Crisis Detection**: Safety-first approach with appropriate resources
- **Privacy-First**: Minimal data collection, guest mode available
- **Mobile-First Design**: Responsive, accessible interface

## Tech Stack

- **Backend**: Python 3.11+, FastAPI, Pydantic, Redis, PostgreSQL
- **Frontend**: Next.js 14, React, Tailwind CSS, shadcn/ui
- **AI**: Simple prompt templates with deterministic outputs
- **Deployment**: Docker, Render/Fly.io ready
- **Auth**: Supabase Auth (passwordless email magic links)

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Redis
- PostgreSQL

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your API keys and database URLs

# Run the backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
cd frontend
npm install

# Set environment variables
cp .env.example .env.local
# Edit .env.local with your backend API URL

# Run the frontend
npm run dev
```

### Docker Setup

```bash
# Run the entire stack
docker-compose up -d

# View logs
docker-compose logs -f
```

## Environment Variables

### Backend (.env)
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/abide
REDIS_URL=redis://localhost:6379

# API Keys
YOUTUBE_API_KEY=your_youtube_api_key
OPENAI_API_KEY=your_openai_api_key  # Optional, for enhanced responses

# App Settings
BIBLE_PROVIDER=public_domain  # public_domain, esv, niv
APP_SECRET_KEY=your_secret_key
ENVIRONMENT=development
```

### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
```

## API Endpoints

- `POST /api/feel` - Submit feelings and get verses/reflection/prayer
- `POST /api/devotion` - Generate 10-minute devotion plan
- `GET /api/history` - Get user's saved items
- `POST /api/save` - Save a response or devotion

## Deployment

### Render
1. Connect your GitHub repository
2. Set environment variables
3. Deploy backend and frontend as separate services

### Fly.io
```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Deploy backend
cd backend
fly launch
fly deploy

# Deploy frontend
cd ../frontend
fly launch
fly deploy
```

## Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm run test
npm run test:e2e
```

## License

This project uses public domain Bible translations (KJV/WEB) by default. ESV and NIV require proper licensing.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Support

For support or questions, please open an issue on GitHub.
