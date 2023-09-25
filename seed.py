from app import app, db
from models import User, Destination, Post, Comment
import random
import uuid

# Create all database tables
db.create_all()

# Seed Users
for i in range(20):
    unique_id = uuid.uuid4()  # Generate a unique ID
    email = f'user{unique_id}@example.com'  # Create a unique email address
    user = User(
        username=f'user{i}',
        password='password',
        email=email
    )
    db.session.add(user)

# Seed Destinations
destinations_data = [
    {"name": "New York City, NY",
     "description": "New York City is a bustling metropolis known for its energy, diversity, and countless attractions. It's divided into five boroughs: Manhattan, Brooklyn, Queens, The Bronx, and Staten Island, each offering its own unique charm."},
    {"name": "Las Vegas, NV",
     "description": "Las Vegas, often referred to as 'Sin City,' is a world-famous destination known for its vibrant nightlife, luxurious resorts, and non-stop entertainment. Located in the Mojave Desert of Nevada, Las Vegas is a city that never sleeps, offering a unique and exciting experience for visitors."},
    {"name": "New Orleans, LA",
     "description": "New Orleans, often called 'The Crescent City' for its position along the winding Mississippi River, is a vibrant and culturally rich destination known for its music, cuisine, and unique blend of traditions. This city in Louisiana offers a one-of-a-kind experience for visitors."},
    {"name": "Key West, FL",
     "description": "Key West is a tropical island paradise located at the southernmost tip of Florida. Known for its stunning natural beauty, vibrant culture, and laid-back atmosphere, Key West offers a unique and relaxing escape for visitors."},
    {"name": "San Diego, CA",
     "description": "San Diego, often referred to as 'America's Finest City,' is a coastal gem located in Southern California. Known for its year-round pleasant weather, stunning beaches, and a diverse range of attractions, San Diego offers a delightful blend of outdoor adventure, cultural richness, and relaxation."},
    {"name": "Savannah, GA",
     "description": "Savannah, often referred to as the 'Hostess City of the South,' is a city rich in history, culture, and Southern hospitality. Nestled along the banks of the Savannah River, this charming coastal city beckons visitors with its cobblestone streets, antebellum architecture, and lush green squares."},
    {"name": "Nashville, TN",
     "description": "Nashville, often referred to as 'Music City, USA,' is a dynamic and vibrant city renowned for its deep musical heritage, live music scene, and Southern charm. Located along the Cumberland River, Nashville is a destination where music fills the air and creativity thrives."},
    {"name": "Charleston, SC",
     "description": "Charleston, often referred to as the 'Holy City' for its abundance of historic churches, is a captivating coastal gem known for its rich history, stunning architecture, and Southern hospitality. Located along the South Carolina coast, Charleston invites visitors to step back in time while enjoying its timeless beauty."},
    {"name": "Orlando, FL",
     "description": "Orlando, often called 'The Theme Park Capital of the World,' is a city known for its family-friendly attractions, entertainment, and sunny weather. Located in Central Florida, Orlando is a place where magic and adventure come to life."},
    {"name": "Chicago, IL",
     "description": "Chicago, often referred to as 'The Windy City,' is a dynamic metropolis known for its bold architecture, rich culture, and vibrant neighborhoods. Situated on the southwestern shore of Lake Michigan, Chicago offers a diverse range of experiences for residents and visitors alike."},
    {"name": "Miami Beach, FL",
     "description": "Miami Beach, located along the southeastern coast of Florida, is a vibrant and iconic destination known for its dazzling beaches, Art Deco architecture, and lively atmosphere. With its blend of cultural diversity and tropical beauty, Miami Beach offers a unique and unforgettable experience."},
    {"name": "Washington, D.C.",
     "description": "Washington, D.C., the capital of the United States, is a city of monumental importance, history, and political significance. Located on the banks of the Potomac River, the city is a vibrant hub of culture, education, and government institutions."},
    {"name": "Austin, TX",
     "description": "Austin, often referred to as the 'Live Music Capital of the World,' is a dynamic and culturally rich city nestled in the heart of Texas. Known for its vibrant music scene, thriving arts community, and outdoor adventures, Austin offers a unique blend of creativity and Texas charm."}
]

# Seed Posts and Comments
for destination in destinations_data:
    # Create the Destination object and add it to the session
    destination_obj = Destination(**destination)
    db.session.add(destination_obj)
    db.session.commit()  # Commit this change

    for _ in range(5):  # Create 5 posts for each destination
        post = Post(
            dest_id=destination_obj.dest_id,  # Access dest_id from the Destination object
            title="Sample Post Title",
            description="Sample Post Description"
        )
        db.session.add(post)
        db.session.commit()
        
        for _ in range(2):  # Create 2 comments for each post
            user_id = random.randint(1, 20)  # Random user_id between 1 and 20
            comment = Comment(
                user_id=user_id,
                post_id=post.post_id,
                description="Sample Comment Description"
            )
            db.session.add(comment)

# Commit all other changes
db.session.commit()
