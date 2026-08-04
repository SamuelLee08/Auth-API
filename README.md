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

  cat >> README.md << 'EOF'

## Swagger UI Example

Interact with your API directly in the browser. Lock icons 🔒 indicate protected routes.

![Swagger UI with Bearer Token Authorization](screenshots/swagger-example.png)

**How to use:**
1. Click **Authorize** button (top right)
2. Paste your JWT access token from `/auth/login`
3. Click **Try it out** on any endpoint
4. Swagger automatically includes the Bearer token in requests

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

EOF
