# Agent Zero Enterprise - Frontend

Modern, production-ready React/Next.js frontend for Agent Zero AI orchestration platform.

## 🚀 Features

- **Next.js 14** with App Router and Server Components
- **TypeScript** for type safety
- **Tailwind CSS** for styling with custom design system
- **shadcn/ui** components for beautiful, accessible UI
- **React Query** for efficient data fetching and caching
- **Zustand** for lightweight state management
- **Socket.io** for real-time WebSocket communication
- **Monaco Editor** for code editing
- **Framer Motion** for smooth animations
- **React Markdown** for rich text rendering

## 📁 Project Structure

```
frontend/
├── app/                      # Next.js app directory
│   ├── (auth)/              # Auth routes (login, register)
│   ├── (dashboard)/         # Main app routes
│   │   ├── agents/          # Agent management
│   │   ├── chat/            # Chat interface
│   │   ├── personas/        # Persona configuration
│   │   └── analytics/       # Analytics dashboard
│   ├── layout.tsx           # Root layout
│   ├── page.tsx             # Landing page
│   ├── providers.tsx        # Global providers
│   └── globals.css          # Global styles
├── components/
│   ├── ui/                  # Reusable UI components
│   ├── chat/                # Chat-specific components
│   ├── agents/              # Agent-related components
│   ├── personas/            # Persona configurator
│   └── layout/              # Layout components
├── lib/
│   ├── api.ts               # API client
│   ├── websocket.ts         # WebSocket client
│   ├── utils.ts             # Utility functions
│   └── hooks/               # Custom React hooks
├── types/
│   └── index.ts             # TypeScript type definitions
├── public/                  # Static assets
└── package.json
```

## 🛠️ Tech Stack

### Core
- **Framework**: Next.js 14 (React 18)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui

### State & Data
- **Server State**: @tanstack/react-query
- **Client State**: Zustand
- **Forms**: React Hook Form + Zod validation
- **Real-time**: Socket.io-client

### Features
- **Code Editor**: Monaco Editor (VS Code)
- **Markdown**: react-markdown with remark/rehype
- **Charts**: Recharts
- **Icons**: Lucide React
- **Animations**: Framer Motion

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ and npm/yarn/pnpm
- Backend API running (see main README)

### Installation

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Copy environment variables
cp .env.local.example .env.local

# Edit .env.local with your API URL
# NEXT_PUBLIC_API_URL=http://localhost:5000
# NEXT_PUBLIC_WS_URL=ws://localhost:5000
```

### Development

```bash
# Start development server
npm run dev

# Open http://localhost:3000
```

### Build

```bash
# Build for production
npm run build

# Start production server
npm start
```

## 🎨 Design System

### Colors

The application uses a semantic color system that adapts to light/dark modes:

- **Primary**: Blue 600 (#2563eb) - Main brand color
- **Secondary**: Violet 500 (#8b5cf6) - Accent color
- **Background**: White/Slate 900 - Main background
- **Muted**: Slate 100/800 - Secondary background
- **Border**: Slate 200/700 - Border color

### Typography

- **Font Family**: Inter (system fallback)
- **Headings**: Bold weights (600-700)
- **Body**: Regular weight (400)
- **Code**: JetBrains Mono

### Spacing

8px grid system for consistent spacing throughout the application.

## 📱 Pages

### Landing Page (`/`)
- Hero section with feature highlights
- Use case showcase
- CTA buttons for signup/login

### Dashboard (`/dashboard`)
- Quick actions (New Chat, Create Agent)
- Recent conversations
- Active agents status
- Usage analytics overview

### Chat Interface (`/chat`)
- Real-time streaming chat
- Message history
- Code execution viewer
- File attachments
- Voice input/output

### Persona Studio (`/personas`)
- Visual persona creator
- Personality trait sliders
- Custom instruction editor
- Template gallery

### Agent Management (`/agents`)
- List all agents
- Agent configuration
- Performance metrics
- Tool usage statistics

### Analytics Dashboard (`/analytics`)
- Token usage tracking
- Cost analysis
- Performance metrics
- Export reports

## 🔌 API Integration

### API Client (`lib/api.ts`)

The API client handles all backend communication with:
- Automatic authentication with JWT
- Token refresh on expiry
- Error handling
- Request/response interceptors

```typescript
import { api } from '@/lib/api';

// Example usage
const personas = await api.listPersonas();
const agent = await api.createAgent(data);
```

### WebSocket Client (`lib/websocket.ts`)

Real-time communication for:
- Streaming agent responses
- Typing indicators
- Multi-user sync
- Connection management

```typescript
import { ws } from '@/lib/websocket';

// Connect
ws.connect(authToken);

// Subscribe to events
ws.on('agent_response_chunk', (data) => {
  console.log(data.chunk);
});

// Send message
ws.sendMessage(sessionId, agentId, message);
```

## 🧩 Key Components

### UI Components (`components/ui/`)

Reusable components following shadcn/ui patterns:
- Button
- Input
- Select
- Dialog
- Card
- Badge
- Avatar
- ... and more

### Custom Hooks (`lib/hooks/`)

- `useAuth` - Authentication state management
- `useAgent` - Agent operations
- `useChat` - Chat functionality
- `usePersona` - Persona management
- `useWebSocket` - WebSocket connection

## 🎯 Features Overview

### 1. Authentication
- Email/password registration
- JWT token-based auth
- Automatic token refresh
- Protected routes

### 2. Persona System
- Pre-built personas (Robotics, Finance, etc.)
- Custom persona creation
- Personality trait configuration
- Domain-specific templates

### 3. Agent Management
- Create/update/delete agents
- Assign personas to agents
- Configure agent settings
- Monitor agent performance

### 4. Real-time Chat
- Streaming responses
- Markdown rendering
- Code syntax highlighting
- File attachments
- Voice input/output

### 5. Analytics
- Usage tracking
- Cost analysis
- Performance metrics
- Exportable reports

## 🌐 Deployment

### Vercel (Recommended)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Production deployment
vercel --prod
```

### Environment Variables

Set these in your deployment platform:

```bash
NEXT_PUBLIC_API_URL=https://your-api.com
NEXT_PUBLIC_WS_URL=wss://your-api.com
```

### Build Settings

- **Framework Preset**: Next.js
- **Build Command**: `npm run build`
- **Output Directory**: `.next`
- **Install Command**: `npm install`
- **Node Version**: 18.x

## 🧪 Testing

```bash
# Run type checking
npm run type-check

# Run linting
npm run lint
```

## 📚 Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [shadcn/ui](https://ui.shadcn.com)
- [React Query](https://tanstack.com/query/latest)
- [Socket.io Client](https://socket.io/docs/v4/client-api/)

## 🤝 Contributing

See the main project [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

## 📄 License

See [LICENSE](../LICENSE) in the root directory.
