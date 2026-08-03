from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase = create_client(supabase_url, supabase_key)

@app.on_event("startup")
async def startup():
    print(f"✓ Server running and connected to Supabase at {supabase_url}")

# Define request/response models
class SignUpRequest(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

# REUSABLE DEPENDENCY (FastAPI middleware for auth)
async def verify_token(authorization: str = Header(None)):
    """Verify JWT token and return user. Use with Depends()."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail={"error": "Access token required"})
    
    token = authorization.split(" ")[1]
    
    try:
        user = supabase.auth.get_user(token)
        return user.user
    except Exception as e:
        raise HTTPException(status_code=401, detail={"error": "Invalid or expired token"})

# POST /auth/signup
@app.post("/auth/signup", status_code=201)
async def signup(data: SignUpRequest):
    if not data.email or not data.password:
        raise HTTPException(status_code=400, detail={"error": "Email and password are required"})
    
    try:
        response = supabase.auth.sign_up({
            "email": data.email,
            "password": data.password
        })
        return response.user
    except Exception as e:
        raise HTTPException(status_code=400, detail={"error": str(e)})

# POST /auth/login
@app.post("/auth/login", status_code=200)
async def login(data: LoginRequest):
    if not data.email or not data.password:
        raise HTTPException(status_code=400, detail={"error": "Email and password are required"})
    
    try:
        response = supabase.auth.sign_in_with_password({
            "email": data.email,
            "password": data.password
        })
        return {
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token,
            "user": response.user
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail={"error": "Invalid login credentials"})

# POST /auth/logout (PROTECTED)
@app.post("/auth/logout", status_code=204)
async def logout(user = Depends(verify_token)):
    try:
        supabase.auth.sign_out()
        return None  # 204 No Content
    except Exception as e:
        raise HTTPException(status_code=400, detail={"error": str(e)})

# GET /public/info
@app.get("/public/info")
async def public_info():
    return {"message": "Welcome stranger! This info is public."}

# GET /protected/profile (USES DEPENDENCY)
@app.get("/protected/profile")
async def protected_profile(user = Depends(verify_token)):
    return {
        "id": user.id,
        "email": user.email,
        "created_at": user.created_at
    }

# GET /protected/dashboard (SAME GUARD, NO NEW AUTH CODE!)
@app.get("/protected/dashboard")
async def protected_dashboard(user = Depends(verify_token)):
    return {
        "dashboard": "You are authenticated!",
        "user_id": user.id,
        "email": user.email
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
