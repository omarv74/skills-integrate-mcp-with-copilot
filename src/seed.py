"""
Seed script to populate the database with initial activities and sample users.

Run this once after setting up the database to load initial data.
"""

from sqlmodel import Session, select
from database import engine, create_db_and_tables
from models import Activity, User, Enrollment

# Initial activities data (from original in-memory store)
SEED_ACTIVITIES = [
    {
        "name": "Chess Club",
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    {
        "name": "Programming Class",
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    {
        "name": "Gym Class",
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    {
        "name": "Soccer Team",
        "description": "Join the school soccer team and compete in matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    {
        "name": "Basketball Team",
        "description": "Practice and play basketball with the school team",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["ava@mergington.edu", "mia@mergington.edu"]
    },
    {
        "name": "Art Club",
        "description": "Explore your creativity through painting and drawing",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["amelia@mergington.edu", "harper@mergington.edu"]
    },
    {
        "name": "Drama Club",
        "description": "Act, direct, and produce plays and performances",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["ella@mergington.edu", "scarlett@mergington.edu"]
    },
    {
        "name": "Math Club",
        "description": "Solve challenging problems and participate in math competitions",
        "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
        "max_participants": 10,
        "participants": ["james@mergington.edu", "benjamin@mergington.edu"]
    },
    {
        "name": "Debate Team",
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 12,
        "participants": ["charlotte@mergington.edu", "henry@mergington.edu"]
    }
]


def seed_database():
    """Populate database with initial activities and enrollments."""
    # Create tables
    create_db_and_tables()

    with Session(engine) as session:
        # Check if data already exists
        existing_activities = session.exec(select(Activity)).first()
        if existing_activities:
            print("Database already seeded. Skipping...")
            return

        # Create activities and users
        for activity_data in SEED_ACTIVITIES:
            activity = Activity(
                name=activity_data["name"],
                description=activity_data["description"],
                schedule=activity_data["schedule"],
                max_participants=activity_data["max_participants"]
            )
            session.add(activity)
            session.commit()
            session.refresh(activity)

            # Create users and enrollments
            for email in activity_data["participants"]:
                # Check if user exists
                user = session.exec(
                    select(User).where(User.email == email)
                ).first()

                if not user:
                    user = User(email=email)
                    session.add(user)
                    session.commit()
                    session.refresh(user)

                # Create enrollment
                enrollment = Enrollment(
                    user_id=user.id,
                    activity_id=activity.id
                )
                session.add(enrollment)

            session.commit()

        print(f"✓ Seeded {len(SEED_ACTIVITIES)} activities with enrollments")


if __name__ == "__main__":
    seed_database()
