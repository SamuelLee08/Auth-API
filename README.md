# Auth-API

Secure authentication API with FastAPI and Supabase Auth.

## Features
- User sign-up and login
- JWT token verification
- Protected routes with Bearer token auth
- Swagger UI documentation
- OWASP compliance

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

Server runs at http://localhost:8000

## API Endpoints

- POST /auth/signup - Register
- POST /auth/login - Login  
- POST /auth/logout - Logout
- GET /public/info - Public data
- GET /protected/profile - Private profile
- GET /protected/dashboard - Dashboard

## Security

- Zero-knowledge password handling (Supabase)
- ECDSA token verification
- Server-side token validation
- OWASP compliance
- Secrets in .env (git-ignored)

## For Defense & AI Security

- Authentication layer for LLM access control
- Tenant isolation
- Token-based stateless auth
- NIST SP 800-63B compliance
- Zero-trust architecture

## License

MIT
