from app import create_app
from database import db

if __name__ == "__main__":
    app = create_app()

    # Create database tables
    with app.app_context():
        db.create_all()
