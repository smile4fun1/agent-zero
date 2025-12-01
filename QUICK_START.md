# 🚀 Quick Start - Agent Zero Enterprise

> Get up and running in 5 minutes!

## Prerequisites

- Python 3.10+
- Node.js 18+
- OpenAI API key (or other LLM provider)

---

## Step 1: Backend Setup (2 minutes)

```bash
# Already in the repo? Good!
cd /workspace

# Install Python dependencies
pip install flask-jwt-extended flask-cors pydantic

# Configure environment (if not done already)
# Add to your .env:
# JWT_SECRET_KEY=your-secret-key-here
# OPENAI_API_KEY=your-openai-key

# Run backend
python run_ui.py

# ✓ Backend running at http://localhost:5000
```

---

## Step 2: Frontend Setup (3 minutes)

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Create environment file
cat > .env.local << EOF
NEXT_PUBLIC_API_URL=http://localhost:5000
NEXT_PUBLIC_WS_URL=ws://localhost:5000
EOF

# Run frontend
npm run dev

# ✓ Frontend running at http://localhost:3000
```

---

## Step 3: Test It! (30 seconds)

```bash
# Open your browser
# http://localhost:3000

# You should see:
# - Beautiful landing page ✓
# - Modern UI with dark mode support ✓
# - Feature showcase ✓
```

---

## Test the API

```bash
# Health check
curl http://localhost:5000/api/v2/health

# Should return:
# {"status":"healthy","version":"2.0.0","service":"agent-zero-enterprise"}
```

---

## What You Have Now

✅ **Backend API v2**
- RESTful endpoints
- WebSocket support
- JWT authentication
- Persona management
- Agent orchestration

✅ **Modern Frontend**
- React + Next.js 14
- TypeScript
- Tailwind CSS
- Beautiful landing page
- Ready for customization

✅ **Pre-built Personas**
- General Assistant
- Robotics Engineer (for Bear Robotics!)
- Financial Analyst
- Software Architect
- Marketing Strategist

---

## Next Steps

### 1. Create Your First Persona (API Example)

```bash
# Get auth token first (register)
curl -X POST http://localhost:5000/api/v2/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "you@example.com",
    "password": "secure-password",
    "name": "Your Name"
  }'

# Save the access_token from response

# List default personas
curl http://localhost:5000/api/v2/personas \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 2. Build the Chat Interface

Edit `frontend/app/chat/page.tsx` (create it):

```typescript
"use client";
import { useState } from 'react';
import { api } from '@/lib/api';

export default function ChatPage() {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');

  const sendMessage = async () => {
    const result = await api.executeAgent('agent-id', {
      message,
      stream: false
    });
    setResponse(result.response);
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Chat with Agent</h1>
      <input
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        className="w-full border rounded p-2 mb-2"
        placeholder="Type your message..."
      />
      <button
        onClick={sendMessage}
        className="bg-primary text-white px-4 py-2 rounded"
      >
        Send
      </button>
      {response && (
        <div className="mt-4 p-4 border rounded">
          {response}
        </div>
      )}
    </div>
  );
}
```

### 3. Customize for Bear Robotics

The Robotics Engineer persona is ready! Use it for:

```python
# In your agent code
from python.api.v2.services.persona_service import PersonaService

# Get the robotics persona
personas = PersonaService.list_personas(user_id, domain='robotics')
robotics_persona = personas[0]  # "Robotics Engineer"

# Use it to create an agent specialized for ROS development
```

---

## Documentation

📚 **Full Guides:**
- [IMPLEMENTATION_SUMMARY.md](./IMPLEMENTATION_SUMMARY.md) - What was built
- [ENTERPRISE_ROADMAP.md](./ENTERPRISE_ROADMAP.md) - Complete roadmap
- [README_ENTERPRISE.md](./README_ENTERPRISE.md) - Detailed guide
- [frontend/README.md](./frontend/README.md) - Frontend docs

---

## Common Issues

### Frontend can't connect to backend

```bash
# Check backend is running
curl http://localhost:5000/api/v2/health

# Check .env.local has correct URL
cat frontend/.env.local
```

### CORS errors

The API v2 has CORS configured for localhost:3000. If you need other origins:

```python
# Edit python/api/v2/__init__.py
CORS(app, resources={
    r"/api/v2/*": {
        "origins": ["http://localhost:3000", "https://your-domain.com"],
        ...
    }
})
```

### Missing dependencies

```bash
# Backend
pip install flask-jwt-extended flask-cors pydantic

# Frontend
cd frontend && npm install
```

---

## Deploy to Production

### Frontend (Vercel)

```bash
cd frontend
vercel --prod
```

### Backend (Railway/Fly.io)

```bash
# Use existing Docker setup
docker build -t agent-zero .
docker run -p 5000:5000 agent-zero
```

---

## Support

- 📖 Read the full documentation
- 🐛 Check existing issues
- 💬 Ask in Discord
- 📧 Email: support@agentzero.ai

---

**That's it! You're ready to build amazing AI-powered applications.** 🎉

Need more details? See [README_ENTERPRISE.md](./README_ENTERPRISE.md)
