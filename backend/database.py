"""
MongoDB database connection and initialization
"""
from motor.motor_asyncio import AsyncIOMotorClient
from backend.config import get_settings

settings = get_settings()

client: AsyncIOMotorClient = None
db = None


async def connect_to_mongo():
    """Create database connection on startup."""
    global client, db
    client = AsyncIOMotorClient(settings.mongodb_url)
    db = client[settings.database_name]

    # Create indexes
    await db.users.create_index("email", unique=True)
    await db.trees.create_index("tree_id", unique=True)
    await db.trees.create_index([("latitude", 1), ("longitude", 1)])
    await db.trees.create_index("elevation")
    await db.trees.create_index("location_name")
    await db.environmental_data.create_index("tree_id")
    await db.environmental_data.create_index("timestamp")

    print("Connected to MongoDB")


async def close_mongo_connection():
    """Close database connection on shutdown."""
    global client
    if client:
        client.close()
        print("Closed MongoDB connection")


def get_database():
    """Return the database instance."""
    return db
