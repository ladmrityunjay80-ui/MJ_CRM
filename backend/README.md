# CRM Backend API

FastAPI-based backend for the CRM system.

## Setup

### Prerequisites
- Python 3.10+
- PostgreSQL 14+

### Installation

1. Create virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run the server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/     # API route handlers
│   │       └── api.py         # API router aggregation
│   ├── core/
│   │   ├── config.py          # Configuration
│   │   ├── database.py        # Database setup
│   │   └── security.py        # JWT & password hashing
│   ├── models/                # SQLAlchemy models
│   ├── schemas/               # Pydantic schemas
│   └── services/              # Business logic (future)
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
└── .env.example              # Environment variables template
```

## API Endpoints

### Authentication
- POST `/api/v1/auth/register` - Register new user
- POST `/api/v1/auth/login` - Login user
- GET `/api/v1/auth/me` - Get current user

### Users
- POST `/api/v1/users/` - Create user
- GET `/api/v1/users/` - List users
- GET `/api/v1/users/{id}` - Get user
- PUT `/api/v1/users/{id}` - Update user
- DELETE `/api/v1/users/{id}` - Delete user

### Leads
- POST `/api/v1/leads/` - Create lead
- GET `/api/v1/leads/` - List leads
- GET `/api/v1/leads/{id}` - Get lead
- PUT `/api/v1/leads/{id}` - Update lead
- DELETE `/api/v1/leads/{id}` - Delete lead

### Contacts
- POST `/api/v1/contacts/` - Create contact
- GET `/api/v1/contacts/` - List contacts
- GET `/api/v1/contacts/{id}` - Get contact
- PUT `/api/v1/contacts/{id}` - Update contact
- DELETE `/api/v1/contacts/{id}` - Delete contact

### Companies
- POST `/api/v1/companies/` - Create company
- GET `/api/v1/companies/` - List companies
- GET `/api/v1/companies/{id}` - Get company
- PUT `/api/v1/companies/{id}` - Update company
- DELETE `/api/v1/companies/{id}` - Delete company

### Deals
- POST `/api/v1/deals/` - Create deal
- GET `/api/v1/deals/` - List deals
- GET `/api/v1/deals/{id}` - Get deal
- PUT `/api/v1/deals/{id}` - Update deal
- DELETE `/api/v1/deals/{id}` - Delete deal

### Activities
- POST `/api/v1/activities/` - Create activity
- GET `/api/v1/activities/` - List activities
- GET `/api/v1/activities/{id}` - Get activity
- PUT `/api/v1/activities/{id}` - Update activity
- DELETE `/api/v1/activities/{id}` - Delete activity

### Products
- POST `/api/v1/products/` - Create product
- GET `/api/v1/products/` - List products
- GET `/api/v1/products/{id}` - Get product
- PUT `/api/v1/products/{id}` - Update product
- DELETE `/api/v1/products/{id}` - Delete product

## Development

### Running tests
```bash
pytest
```

### Database migrations (using Alembic - to be set up)
```bash
alembic upgrade head
```

## Security

- JWT authentication
- Password hashing with bcrypt
- Role-based access control (RBAC)
- CORS enabled for frontend
