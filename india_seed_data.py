"""
India Seed Script
Adds Indian tea tree dataset without deleting existing data.

Usage:
python india_seed_data.py
"""

import asyncio
import uuid
import random
from datetime import datetime, timedelta

from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from backend.config import get_settings


settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_india_trees():
    """Generate 10 Indian tea tree records"""

    now = datetime.utcnow()

    india_data = [
        {"height": 11.2, "diameter": 44.6, "ring_count": 120, "elevation": 1500, "latitude": 26.7500, "longitude": 94.2000, "location_name": "Jorhat"},
        {"height": 10.5, "diameter": 38.9, "ring_count": 105, "elevation": 1450, "latitude": 26.8700, "longitude": 94.6300, "location_name": "Assam"},
        {"height": 12.8, "diameter": 55.2, "ring_count": 160, "elevation": 1700, "latitude": 27.0300, "longitude": 88.2700, "location_name": "Darjeeling"},
        {"height": 9.6, "diameter": 33.7, "ring_count": 90, "elevation": 1600, "latitude": 27.0900, "longitude": 88.4700, "location_name": "Kurseong"},
        {"height": 14.1, "diameter": 61.3, "ring_count": 180, "elevation": 1750, "latitude": 27.0400, "longitude": 88.2600, "location_name": "Darjeeling Hills"},
        {"height": 8.9, "diameter": 29.4, "ring_count": 75, "elevation": 1850, "latitude": 11.4100, "longitude": 76.7000, "location_name": "Nilgiri Hills"},
        {"height": 11.7, "diameter": 47.8, "ring_count": 130, "elevation": 1720, "latitude": 11.3600, "longitude": 76.7300, "location_name": "Ooty"},
        {"height": 13.3, "diameter": 54.6, "ring_count": 155, "elevation": 1680, "latitude": 11.3300, "longitude": 76.7700, "location_name": "Coonoor"},
        {"height": 10.2, "diameter": 40.1, "ring_count": 110, "elevation": 1520, "latitude": 26.9800, "longitude": 94.6200, "location_name": "Dibrugarh"},
        {"height": 9.1, "diameter": 31.8, "ring_count": 85, "elevation": 1780, "latitude": 11.4500, "longitude": 76.6400, "location_name": "Kotagiri"},
    ]

    trees = []

    for t in india_data:
        trees.append({
            "tree_id": str(uuid.uuid4()),
            "height": t["height"],
            "diameter": t["diameter"],
            "ring_count": t["ring_count"],
            "elevation": t["elevation"],
            "latitude": t["latitude"],
            "longitude": t["longitude"],
            "location_name": t["location_name"],
            "country": "India",
            "images": [],
            "created_by": "india_seed",
            "created_at": now,
            "updated_at": now,
        })

    return trees


def generate_environmental_data(trees):
    """Generate environmental data for trees"""

    now = datetime.utcnow()
    records = []

    for tree in trees:
        for i in range(3):
            records.append({
                "record_id": str(uuid.uuid4()),
                "tree_id": tree["tree_id"],
                "temperature": round(random.uniform(12, 30), 1),
                "humidity": round(random.uniform(60, 95), 1),
                "wind_speed": round(random.uniform(1, 7), 1),
                "co2_level": round(random.uniform(380, 440), 1),
                "timestamp": now - timedelta(days=random.randint(0, 120)),
            })

    return records


async def seed():

    print("🌿 Connecting to MongoDB...")

    client = AsyncIOMotorClient(settings.mongodb_url)
    db = client[settings.database_name]

    print("🌳 Generating India tea tree dataset...")

    trees = generate_india_trees()

    await db.trees.insert_many(trees)

    print(f"Inserted {len(trees)} Indian tea tree records")

    print("🌡️ Generating environmental data...")

    env_records = generate_environmental_data(trees)

    await db.environmental_data.insert_many(env_records)

    print(f"Inserted {len(env_records)} environmental records")

    print("📇 Ensuring indexes exist...")

    await db.trees.create_index("tree_id", unique=True)
    await db.trees.create_index([("latitude", 1), ("longitude", 1)])
    await db.trees.create_index("location_name")
    await db.environmental_data.create_index("tree_id")

    print("\n✅ India dataset added successfully")
    print(f"Trees added: {len(trees)}")
    print(f"Environmental records added: {len(env_records)}")

    client.close()


if __name__ == "__main__":
    asyncio.run(seed())