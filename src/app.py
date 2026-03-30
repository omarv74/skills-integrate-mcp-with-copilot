"""
High School Management System API

A FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.

This version uses SQLite for persistent data storage.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select
import os
from pathlib import Path

from database import engine, get_session, create_db_and_tables
from models import Activity, User, Enrollment
from seed import seed_database

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Create database tables and seed data on startup
@app.on_event("startup")
def on_startup():
    """Initialize database with seed data on first run."""
    create_db_and_tables()
    seed_database()

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities(session: Session = Depends(get_session)):
    """Retrieve all activities with participant count and availability."""
    activities_list = session.exec(select(Activity)).all()
    
    result = {}
    for activity in activities_list:
        # Count enrollments for this activity
        participant_count = session.exec(
            select(Enrollment).where(Enrollment.activity_id == activity.id)
        ).all()
        
        # Get participant emails
        participant_emails = [e.user.email for e in participant_count]
        
        result[activity.name] = {
            "description": activity.description,
            "schedule": activity.schedule,
            "max_participants": activity.max_participants,
            "participants": participant_emails
        }
    
    return result


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(
    activity_name: str,
    email: str,
    session: Session = Depends(get_session)
):
    """Sign up a student for an activity."""
    # Find activity by name
    activity = session.exec(
        select(Activity).where(Activity.name == activity_name)
    ).first()
    
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Check if student already enrolled
    existing_enrollment = session.exec(
        select(Enrollment)
        .where(Enrollment.activity_id == activity.id)
    ).all()
    
    for enrollment in existing_enrollment:
        if enrollment.user.email == email:
            raise HTTPException(
                status_code=400,
                detail="Student is already signed up"
            )
    
    # Check capacity
    if len(existing_enrollment) >= activity.max_participants:
        raise HTTPException(
            status_code=400,
            detail="Activity is at maximum capacity"
        )

    # Get or create user
    user = session.exec(
        select(User).where(User.email == email)
    ).first()
    
    if not user:
        user = User(email=email)
        session.add(user)
        session.commit()
        session.refresh(user)

    # Create enrollment
    enrollment = Enrollment(user_id=user.id, activity_id=activity.id)
    session.add(enrollment)
    session.commit()
    
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(
    activity_name: str,
    email: str,
    session: Session = Depends(get_session)
):
    """Unregister a student from an activity."""
    # Find activity by name
    activity = session.exec(
        select(Activity).where(Activity.name == activity_name)
    ).first()
    
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Find and remove enrollment
    enrollment = session.exec(
        select(Enrollment).where(Enrollment.activity_id == activity.id)
    ).all()
    
    for enroll in enrollment:
        if enroll.user.email == email:
            session.delete(enroll)
            session.commit()
            return {"message": f"Unregistered {email} from {activity_name}"}

    raise HTTPException(
        status_code=400,
        detail="Student is not signed up for this activity"
    )
