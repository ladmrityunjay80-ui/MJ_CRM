# CRM Frontend

React + TypeScript + Vite frontend for the CRM system.

## Setup

### Prerequisites
- Node.js 18+
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API URL
```

3. Run the development server:
```bash
npm run dev
```

## Project Structure

```
frontend/
├── src/
│   ├── components/       # Reusable components
│   ├── lib/             # Utilities (API client, auth store)
│   ├── pages/           # Page components
│   ├── services/        # API service functions
│   ├── types/           # TypeScript type definitions
│   ├── App.tsx          # Main app component with routing
│   └── main.tsx         # Entry point
├── public/              # Static assets
└── package.json         # Dependencies
```

## Features

- Authentication (login/register)
- Protected routes
- Dashboard with stats
- Leads management
- Responsive sidebar navigation
- API integration with React Query
- State management with Zustand

## Tech Stack

- React 18 with TypeScript
- Vite for build tooling
- React Router for routing
- TanStack Query for data fetching
- Zustand for state management
- TailwindCSS for styling
- Lucide React for icons
- Axios for API calls
