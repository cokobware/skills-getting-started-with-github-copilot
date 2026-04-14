"""
High School Management System API

A simple FastAPI app that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="Mergington High School API",
    description="API for viewing and signing up for extracurricular activities",
)

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(current_dir, "static")),
    name="static",
)

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"],
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"],
    },
    # Sports
    "Soccer Team": {
        "description": "Competitive soccer practices and matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 22,
        "participants": [],
    },
    "Basketball Club": {
        "description": "Skill drills, pickup games, and intramural tournaments",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:30 PM",
        "max_participants": 15,
        "participants": [],
    },
    # Artistic
    "Art Club": {
        "description": "Painting, drawing, and creative workshops",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": [],
    },
    "Drama Society": {
        "description": "Acting, stagecraft, and production of school plays",
        "schedule": "Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 25,
        "participants": [],
    },
    # Intellectual
    "Debate Team": {
        "description": "Learn debate formats, research, and inter-school competitions",
        "schedule": "Wednesdays, 5:00 PM - 6:30 PM",
        "max_participants": 12,
        "participants": [],
    },
    "Science Olympiad": {
        "description": "Prepare for regional science competitions and hands-on labs",
        "schedule": "Saturdays, 9:00 AM - 12:00 PM",
        "max_participants": 20,
        "participants": [],
    },
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]

    # Check capacity
    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(status_code=400, detail="Activity is full")

    # Check duplicate signup
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up")

    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
