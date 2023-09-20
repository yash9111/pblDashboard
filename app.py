from fastapi import FastAPI, HTTPException
import firebase_admin
from firebase_admin import auth
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("confedential/private.json")
firebase_admin.initialize_app(cred)



app = FastAPI()

@app.post("/login")
async def login(user_id: str, password: str):
    try:
        # Authenticate with Firebase
        user_id=user_id+'@mail.com'
        user = auth.get_user_by_email(user_id)

        print(user)

        return {"message": "Login successful", "user_id": user_id}
    except auth.UserNotFoundError:
        raise HTTPException(status_code=401, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))