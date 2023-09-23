from fastapi import FastAPI, HTTPException, File, UploadFile,Depends,Query
import firebase_admin
from firebase_admin import auth, credentials, storage,firestore,initialize_app
import os
from typing import List

app = FastAPI()

# Initialize Firebase Admin SDK with your service account credentials and specify the storage bucket
cred = credentials.Certificate("confedential/private.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'pbldashboard.appspot.com'  # Replace with your actual bucket name
})


db = firestore.client()



def create_project(project_id, title, description, resources_link, repo_link, faculty_users, student_users):
    try:
        # Reference to the "Projects" collection
        projects_ref = db.collection("Projects")

        # Create a new project document with the specified project ID
        project_data = {
            "project_id": project_id,
            "title": title,
            "description": description,
            "resources_link": resources_link,
            "repo_link": repo_link,
            "faculty_users": faculty_users,
            "student_users": student_users
        }

        # Add the project document to Firestore
        projects_ref.add(project_data)

        return f"Project created with ID: {project_id}"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




# create_project(
#     project_id="Car",
#     title="Car Automation Project",
#     description="A test project",
#     resources_link="https://example.com/resources",
#     repo_link="https://github.com/sample/repo",
#     faculty_users=["Sanskar","Sanskar1"],
#     student_users=["yash",]
# )


def get_user_projects(user_id: str):
    projects_ref = db.collection("Projects")
    query = projects_ref.where("faculty_users", "array_contains", user_id).stream()
    print(query)
    
    faculty_projects = [project.to_dict() for project in query]

    query = projects_ref.where("student_users", "array_contains", user_id).stream()
    print(query)
    student_projects = [project.to_dict() for project in query]
    print(student_projects)
    # Combine faculty and student projects into a single list
    all_projects = faculty_projects + student_projects

    return {"user_projects": all_projects}

print(get_user_projects("Yash")
)