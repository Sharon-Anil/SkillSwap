# seed_dummy_data.py

from app import db, create_app
from app.models import User, Video

app = create_app()

with app.app_context():
    # OPTIONAL: Clean start (uncomment if needed)
    # db.drop_all()
    # db.create_all()

    # Check if creators already exist
    if not User.query.filter_by(channel_name="ArtZone").first():
        # Create creator users
        creator1 = User(username="artzoneuser", email="art@demo.com", password="test", role="creator", channel_name="ArtZone", category="Art")
        creator2 = User(username="codemasteruser", email="code@demo.com", password="test", role="creator", channel_name="CodeMaster", category="Coding")

        db.session.add_all([creator1, creator2])
        db.session.commit()

        # Add videos for ArtZone
        video1 = Video(title="Sketch Basics", description="Learn sketching", filename="sketch.mp4", is_free=True, creator_id=creator1.id)
        video2 = Video(title="Advanced Art", description="Shading tutorial", filename="shading.mp4", coin_required=5, is_free=False, creator_id=creator1.id)

        # Add videos for CodeMaster
        video3 = Video(title="Python for Beginners", description="Intro to Python", filename="python.mp4", is_free=True, creator_id=creator2.id)
        video4 = Video(title="Ethical Hacking", description="XSS explained", filename="xss.mp4", coin_required=10, is_free=False, creator_id=creator2.id)

        db.session.add_all([video1, video2, video3, video4])
        db.session.commit()

        print("✅ Dummy creators and videos added.")
    else:
        print("ℹ️ Dummy data already exists.")
