# Quickstart: RAG Chatbot Development

**Feature**: 001-rag-chatbot | **For**: Developers joining the project

---

## Overview

This guide gets you up and running with the RAG chatbot development environment in under 15 minutes.

---

## Prerequisites

| Requirement | Version | Why |
|-------------|---------|-----|
| Python | 3.11+ | Backend FastAPI server |
| Node.js | 20+ | Docusaurus frontend |
| Git | Latest | Version control |
| OpenAI API Key | - | Get from platform.openai.com |
| Qdrant Cloud Account | Free Tier | Sign up at qdrant.tech |
| Neon Postgres Account | Free Tier | Sign up at neon.tech |

---

## Step 1: Backend Setup (5 minutes)

### 1.1 Create Virtual Environment

```bash
# From repository root
cd backend
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

### 1.2 Install Dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt**:
```text
fastapi==0.109.0
uvicorn[standard]==0.27.0
httpx==0.26.0
qdrant-client==1.9.0
openai==1.12.0
psycopg2-binary==2.9.9
python-dotenv==1.0.0
tiktoken==0.5.2
pydantic==2.6.0
pytest==8.0.0
pytest-asyncio==0.23.4
```

### 1.3 Configure Environment Variables

Create `backend/.env`:
```bash
# Qdrant Cloud
QDRANT_URL=https://e2bc507b-953a-453d-a847-735aa2ee1988.us-east4-0.gcp.cloud.qdrant.io:6333
QDRANT_API_KEY=your_qdrant_api_key_here

# OpenAI
OPENAI_API_KEY=your_openai_api_key_here

# Neon Postgres
NEON_DATABASE_URL=postgresql://user:pass@host/db?sslmode=require

# CORS (allow Docusaurus on GitHub Pages)
CORS_ORIGINS=https://soban-saleem.github.io
```

### 1.4 Verify Backend

```bash
# Run health check
python -m app.main

# Or using uvicorn directly
uvicorn app.main:app --reload
```

Visit http://localhost:8000/health - should return healthy status.

---

## Step 2: Index Content (3 minutes)

### 2.1 Run Indexing Script

```bash
python scripts/index_content.py --docs-path ../docs
```

This will:
1. Parse all markdown files in `docs/`
2. Chunk into 300-500 token semantic paragraphs
3. Generate embeddings via OpenAI
4. Store in Qdrant Cloud

### 2.2 Verify Index

```bash
curl https://your-cluster.us-east4-0.gcp.cloud.qdrant.io:6333/collections/textbook_chunks
```

Should return collection info with `points_count > 0`.

---

## Step 3: Frontend Setup (5 minutes)

### 3.1 Install Docusaurus Dependencies

```bash
# From repository root
npm install
```

### 3.2 Create Chatbot Component

Create `src/chatbot/SidebarChatbot.tsx`:
```typescript
import React, { useState } from 'react';

export default function SidebarChatbot() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);

  return (
    <>
      <button onClick={() => setIsOpen(!isOpen)}>
        {isOpen ? 'Close' : 'Ask AI'}
      </button>
      {isOpen && (
        <div className="chatbot-sidebar">
          {/* Chat UI goes here */}
        </div>
      )}
    </>
  );
}
```

### 3.3 Register Client Module

Add to `docusaurus.config.js`:
```javascript
export default {
  // ... existing config
  clientModules: [require.resolve('./src/chatbot/bootstrap.js')],
};
```

Create `src/chatbot/bootstrap.js`:
```javascript
import SidebarChatbot from './SidebarChatbot';

// Inject into Docusaurus layout
// (Implementation details in plan.md)
```

---

## Step 4: Run Integration (2 minutes)

### 4.1 Start Both Services

```bash
# Terminal 1: Backend
cd backend
uvicorn app.main:app --reload

# Terminal 2: Frontend
npm run start
```

### 4.2 Test Chat

1. Open http://localhost:3000
2. Navigate to any lesson page
3. Click "Ask AI" button in sidebar
4. Type: "What is Physical AI?"
5. Should receive answer with citation

---

## Common Issues

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'app'` | Run from `backend/` directory |
| Qdrant connection timeout | Check `QDRANT_URL` and `QDRANT_API_KEY` in `.env` |
| OpenAI rate limit error | Wait 60 seconds or check API key quota |
| CORS errors in browser | Verify `CORS_ORIGINS` matches your frontend URL |
| Empty search results | Run `scripts/index_content.py` to populate Qdrant |

---

## Project Structure Reference

```
Physical_AI_Humanoid_Robotics_Textbook/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── api/               # Chat endpoints
│   │   ├── services/          # RAG pipeline
│   │   └── models/            # Pydantic schemas
│   ├── scripts/               # Indexing, utilities
│   └── tests/                 # Backend tests
├── src/                        # Frontend components
│   └── chatbot/               # React chat widget
├── docs/                       # Textbook content (indexed)
├── specs/001-rag-chatbot/     # This plan
└── docusaurus.config.js        # Site config
```

---

## Next Steps

1. **Phase 1**: Content Indexing → Run `scripts/index_content.py`
2. **Phase 2**: Backend API → Implement `/chat` endpoint
3. **Phase 3**: Frontend Widget → Build React sidebar component
4. **Phase 4**: Integration → Connect widget to API
5. **Phase 5**: Deployment → Deploy backend to Railway

See `plan.md` for detailed implementation tasks.

---

## Getting Help

| Resource | Link |
|----------|------|
| Full Specification | `specs/001-rag-chatbot/spec.md` |
| API Documentation | `specs/001-rag-chatbot/contracts/api.yaml` |
| Data Model | `specs/001-rag-chatbot/data-model.md` |
| Research Decisions | `specs/001-rag-chatbot/research.md` |
| Implementation Tasks | `specs/001-rag-chatbot/tasks.md` (after `/sp.tasks`) |
