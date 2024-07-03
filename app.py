from fastapi import FastAPI, HTTPException, File, UploadFile,Depends,Query
import firebase_admin
from firebase_admin import auth, credentials, storage,firestore,initialize_app
import os
from typing import List
from mailjet_rest import Client



app = FastAPI()

# Initialize Firebase Admin SDK with your service account credentials and specify the storage bucket
cred = credentials.Certificate("confedential/private.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'pbldashboard.appspot.com'  # Replace with your actual bucket name
})

db = firestore.client()

# ==================================================================================


# ==================================================================================

# users_ref = db.collection("users")
# files_ref = db.collection("files")
# associations_ref = db.collection("user_file_associations")


# def upload_file_to_firebase_storage(file_path):
#     bucket = storage.bucket()
#     blob = bucket.blob(os.path.basename(file_path))

#     # Upload the file to Firebase Storage
#     blob.upload_from_filename(file_path)

#     print(f"File {os.path.basename(file_path)} uploaded to Firebase Storage")


###########CHECKED##########################
@app.post("/login")
async def login(user_id: str, password: str):
    try:
        user_id = user_id + '@mail.com'
        user = auth.get_user_by_email(user_id)

        print(user)

        return {"message": "Login successful", "user_id": user_id}
    except auth.UserNotFoundError:
        raise HTTPException(status_code=401, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# ================================================================================
@app.post("/add-project/")
async def add_project(
    project_id: str,
    title: str,
    description: str,
    resources_link: str,
    repo_link: str,
    faculty_users: list,
    student_users: list
):
    result = create_project(
        project_id, title, description, resources_link, repo_link, faculty_users, student_users
    )
    return {"message": result}

# ======================================================================

# Endpoint to retrieve all projects
#################CHECKED#################################
@app.get("/projects/")
async def get_all_projects():
    projects_ref = db.collection("Projects")
    projects = projects_ref.stream()
    project_list = [project.to_dict() for project in projects]
    return {"projects": project_list}

# ===============================================================================

# Endpoint to retrieve projects associated with a user

##################CHECKED###############################
@app.get("/user-projects/")
async def get_user_projects(user_id: str):
    projects_ref = db.collection("Projects")
    query = projects_ref.where("faculty_users", "array_contains", user_id).stream()
    faculty_projects = [project.to_dict() for project in query]

    query = projects_ref.where("student_users", "array_contains", user_id).stream()
    student_projects = [project.to_dict() for project in query]
    print(student_projects)
    # Combine faculty and student projects into a single list
    all_projects = faculty_projects + student_projects

    return {"user_projects": all_projects}

# ================================================================================
# Endpoint to add or remove a user from a project

@app.put("/update-project-users/")
async def update_project_users(
    project_id: str,
    user_id: str,
    add_user: bool = Query(False, description="Set to true to add the user, false to remove")
):
    try:
        # Reference to the specific project document
        project_ref = db.collection("Projects").document(project_id)

        # Get the current project data
        project_data = project_ref.get().to_dict()

        # Update faculty or student users based on the add_user flag
        if add_user:
            if user_id not in project_data["faculty_users"]:
                project_data["faculty_users"].append(user_id)
        else:
            if user_id in project_data["faculty_users"]:
                project_data["faculty_users"].remove(user_id)

        # Update the project document in Firestore
        project_ref.set(project_data)

        return {"message": "User added to project" if add_user else "User removed from project"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ======================================================================================


@app.post("/send-email/")
def send_email(sender:str,reciver:str,project_id:str):
        
    api_key = "8d668ef429f0c394d4a2fab1f5e91f60"
    api_secret = "d4e83a1fc798f66b654adc51421823eb"

    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    data = {
    'Messages': [
                    {
                            "From": {
                                    "Email": sender,
                                    "Name": sender
                            },
                            "To": [
                                    {
                                            "Email": reciver,
                                            "Name": "aashu"
                                    }
                            ],
                            "Subject": "Request for opting your project",
                            "TextPart": "hey , i want to opt into your project named "+project_id,
                    }
            ]
    }
    result = mailjet.send.create(data=data)
    print (result.status_code)
    print (result.json())
