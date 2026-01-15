# RAG Chatbot Backend

FastAPI backend for the Physical AI textbook RAG chatbot. Provides question-answering with source citations using OpenAI embeddings and Qdrant vector storage.

## Features

- **RAG (Retrieval-Augmented Generation)**: Answers questions using indexed textbook content
- **Text Selection Mode**: Constrains answers to user-selected text
- **Conversation Memory**: Maintains context for follow-up questions
- **Source Citations**: Returns references to source material
- **Caching**: Reduces API costs with smart response caching
- **Circuit Breaker**: Prevents cascade failures during outages

## Tech Stack

- **FastAPI**: Async Python web framework
- **OpenAI**: `text-embedding-3-small` (1536 dims), `gpt-4o-mini`
- **Qdrant Cloud**: Vector similarity search
- **Neon Postgres** (optional): Analytics logging
- **Pytest**: Testing framework

## Local Development

### Prerequisites

- Python 3.11+
- Poetry or pip
- Qdrant Cloud account (or local Qdrant)
- OpenAI API key

### Setup

1. **Clone and navigate:**
   ```bash
   cd backend
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   # or with poetry:
   poetry install
   ```

3. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

   Required variables:
   ```bash
   OPENAI_API_KEY=sk-...
   QDRANT_URL=https://your-cluster.qdrant.io
   QDRANT_API_KEY=...
   NEON_DATABASE_URL=postgresql://...  # optional
   CORS_ORIGINS=http://localhost:3000
   ```

4. **Run the development server:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   API will be available at `http://localhost:8000`

5. **View API docs:**
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

## Indexing Content

Before the chatbot can answer questions, you need to index the textbook content:

```bash
# From backend directory
python scripts/reindex.py
```

This will:
- Scan all markdown files in `../docs/`
- Chunk content into semantic segments
- Generate embeddings
- Upload to Qdrant

### Validate Index

Check if indexing was successful:

```bash
python scripts/validate_index.py
```

## API Endpoints

### `POST /chat`
Answer a question about the textbook.

**Request:**
```json
{
  "question": "What is LIDAR?",
  "sessionId": "optional-session-id",
  "contextMessages": []  // optional conversation history
}
```

**Response:**
```json
{
  "answer": "LIDAR (Light Detection and Ranging) is...",
  "citations": [
    {
      "citationId": "cite_001",
      "moduleId": "module1-sensors",
      "lessonTitle": "Introduction to Sensors",
      "sectionHeading": "LIDAR",
      "urlAnchor": "/module1/sensors#lidar",
      "relevanceScore": 0.92
    }
  ],
  "sessionId": "session-abc",
  "isCached": false
}
```

### `POST /chat/selection`
Answer based on selected text only.

**Request:**
```json
{
  "question": "What does this mean?",
  "selectedText": "LIDAR is a remote sensing method...",
  "pageUrl": "/docs/module1/sensors",
  "sessionId": "optional"
}
```

### `GET /health`
Check service health status.

**Response:**
```json
{
  "status": "healthy",
  "services": {
    "qdrant": true,
    "openai": true,
    "neon": false
  },
  "timestamp": 1234567890
}
```

## Testing

### Run all tests:
```bash
pytest
```

### Run specific test file:
```bash
pytest tests/test_chunking.py
```

### Run with coverage:
```bash
pytest --cov=app --cov-report=html
```

### Test categories:
- `test_config.py` - Configuration validation
- `test_health.py` - Health check endpoint
- `test_chunking.py` - Markdown chunking
- `test_services.py` - Core services (embedding, retrieval, generation, citation)
- `test_api.py` - API endpoints
- `test_selection.py` - Text-selection mode
- `test_context.py` - Conversation context
- `test_integration.py` - End-to-end pipeline

## Manual Frontend Testing

Since the frontend is a React widget integrated into Docusaurus, manual testing requires running the full site.

### Browser Dev Tools Testing

1. **Start the backend:**
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Start Docusaurus (from project root):**
   ```bash
   npm run start
   ```

3. **Test the chatbot:**
   - Navigate to `http://localhost:3000`
   - Click the chat toggle button (top-right)
   - Ask a question about the content

### Network Tab Testing

1. Open browser DevTools (F12)
2. Go to Network tab
3. Send a chat question
4. Inspect the `/chat` request:
   - Status should be 200
   - Response should include `answer` and `citations`
   - Check request payload includes `contextMessages` for follow-ups

### Responsive Testing

Test at different breakpoints:
- **Desktop** (>768px): Sidebar on right
- **Mobile** (<768px): Full-screen overlay

Chrome DevTools: Toggle device toolbar (Cmd+Shift+M)

### Accessibility Testing

#### Keyboard Navigation
- Tab to chat input
- Enter to submit
- Escape to close sidebar (mobile)

#### ARIA Labels
Check using Chrome DevTools:
1. Elements tab → Accessibility pane
2. Verify chatbot has `role="complementary"`
3. Verify `aria-label="Course assistant chatbot"`

#### Screen Reader Testing
- macOS: VoiceOver (Cmd+F5)
- Windows: Narrator (Win+Ctrl+Enter)

### Accessibility Audits

Run automated audits:

**Lighthouse:**
1. Open DevTools → Lighthouse tab
2. Choose "Accessibility"
3. Run audit

**Axe DevTools:**
1. Install Axe DevTools extension
2. Click "Scan ALL of my page"
3. Review violations

Common issues to check:
- Color contrast (WCAG AA requires 4.5:1)
- Focus indicators (visible outline)
- Keyboard traps (Escape to close modals)
- ARIA labels on interactive elements

## Deployment

### Railway (Recommended)

1. Connect GitHub repo to Railway
2. Create new project from `backend/` directory
3. Set environment variables in Railway dashboard
4. Deploy!

### Docker

```bash
docker build -t rag-chatbot-backend .
docker run -p 8000:8000 --env-file .env rag-chatbot-backend
```

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | OpenAI API key |
| `QDRANT_URL` | Yes | Qdrant cluster URL |
| `QDRANT_API_KEY` | Yes | Qdrant API key |
| `NEON_DATABASE_URL` | No | Postgres for analytics |
| `CORS_ORIGINS` | Yes | Allowed frontend origins |

## Architecture

```
┌─────────────┐
│   Frontend  │ (React + Docusaurus)
└──────┬──────┘
       │ HTTP/JSON
       ▼
┌───────────────────────────────────┐
│           FastAPI                 │
│  ┌─────────────────────────────┐  │
│  │  API Routes (/chat, /health) │  │
│  └───────────┬─────────────────┘  │
│              ▼                     │
│  ┌─────────────────────────────┐  │
│  │  Services                   │  │
│  │  • Chunking                 │  │
│  │  • Embedding (OpenAI)        │  │
│  │  • Retrieval (Qdrant)        │  │
│  │  • Generation (OpenAI)       │  │
│  │  • Citation                 │  │
│  └─────────────────────────────┘  │
└───────────────────────────────────┘
       │                    │
       ▼                    ▼
┌─────────────┐      ┌─────────────┐
│   Qdrant    │      │   OpenAI    │
│ (Vector DB) │      │    API      │
└─────────────┘      └─────────────┘
```

## Troubleshooting

### Qdrant connection fails
- Verify `QDRANT_URL` and `QDRANT_API_KEY` in `.env`
- Check network allows connection to Qdrant Cloud
- Try `curl $QDRANT_URL` to test connectivity

### OpenAI rate limit errors
- Check API key has sufficient quota
- Implement request queuing for high traffic
- Circuit breaker will auto-recover after 60 seconds

### Empty search results
- Run `python scripts/validate_index.py`
- Ensure content has been indexed with `reindex.py`
- Check `score_threshold` isn't too high

### CORS errors
- Add frontend URL to `CORS_ORIGINS` in `.env`
- Format: `http://localhost:3000,https://yourdomain.com`

## License

MIT
