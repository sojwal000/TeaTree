"""
Seed script: populates the MongoDB database with sample wild tea tree data
for development and demonstration purposes.

Usage: python seed_data.py
"""
import asyncio
import random
import uuid
from datetime import datetime, timedelta

from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from backend.config import get_settings

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ── Locations with realistic coordinates (Yunnan, China tea regions) ──────────
LOCATIONS = [
    {"name": "Xishuangbanna", "lat": 21.98, "lon": 100.80, "elev_base": 1200},
    {"name": "Pu'er", "lat": 22.82, "lon": 100.97, "elev_base": 1400},
    {"name": "Lincang", "lat": 23.88, "lon": 100.09, "elev_base": 1600},
    {"name": "Menghai", "lat": 21.97, "lon": 100.45, "elev_base": 1300},
    {"name": "Jingmai Mountain", "lat": 22.12, "lon": 99.98, "elev_base": 1800},
    {"name": "Bulang Mountain", "lat": 21.62, "lon": 100.40, "elev_base": 1700},
    {"name": "Wuliang Mountain", "lat": 24.45, "lon": 100.83, "elev_base": 2000},
    {"name": "Ailao Mountain", "lat": 24.10, "lon": 101.50, "elev_base": 2200},
    {"name": "Banzhang", "lat": 21.75, "lon": 100.52, "elev_base": 1500},
    {"name": "Yiwu", "lat": 22.05, "lon": 101.47, "elev_base": 1350},
    {"name": "Nannuo Mountain", "lat": 21.87, "lon": 100.65, "elev_base": 1600},
    {"name": "Bada Mountain", "lat": 21.58, "lon": 100.12, "elev_base": 1900},
]


def generate_trees(n=300):
    """Generate n sample tea tree records."""
    trees = []
    now = datetime.utcnow()

    for i in range(n):
        loc = random.choice(LOCATIONS)
        elevation = loc["elev_base"] + random.uniform(-200, 400)
        diameter = random.uniform(10, 120) + (elevation / 100) * random.uniform(0.1, 0.5)
        height = diameter * random.uniform(0.15, 0.35) + random.uniform(1, 5)
        ring_count = int(diameter * random.uniform(1.5, 3.5) + random.uniform(-10, 30))

        trees.append({
            "tree_id": str(uuid.uuid4()),
            "height": round(height, 2),
            "diameter": round(diameter, 2),
            "ring_count": max(ring_count, 5) if random.random() > 0.15 else None,  # 15% missing
            "elevation": round(elevation, 1),
            "latitude": round(loc["lat"] + random.uniform(-0.15, 0.15), 6),
            "longitude": round(loc["lon"] + random.uniform(-0.15, 0.15), 6),
            "location_name": loc["name"],
            "images": [],
            "created_by": "seed",
            "created_at": now - timedelta(days=random.randint(0, 365)),
            "updated_at": now,
        })
    return trees


def generate_environmental_data(trees, records_per_tree=3):
    """Generate environmental data linked to trees."""
    records = []
    now = datetime.utcnow()

    for tree in trees:
        for j in range(random.randint(1, records_per_tree)):
            records.append({
                "record_id": str(uuid.uuid4()),
                "tree_id": tree["tree_id"],
                "temperature": round(random.uniform(10, 30) - tree["elevation"] / 500, 1),
                "humidity": round(random.uniform(55, 95), 1),
                "wind_speed": round(random.uniform(0.5, 8.0), 1),
                "co2_level": round(random.uniform(380, 450), 1),
                "timestamp": now - timedelta(days=random.randint(0, 180), hours=random.randint(0, 23)),
            })
    return records


async def seed():
    print("🌿 Connecting to MongoDB...")
    client = AsyncIOMotorClient(settings.mongodb_url)
    db = client[settings.database_name]

    # Clear existing data
    print("🗑️  Clearing existing data...")
    await db.users.delete_many({})
    await db.trees.delete_many({})
    await db.environmental_data.delete_many({})

    # Create demo user
    print("👤 Creating demo user...")
    demo_user = {
        "user_id": str(uuid.uuid4()),
        "name": "Demo Researcher",
        "email": "demo@teatree.org",
        "password_hash": pwd_context.hash("demo123"),
        "created_at": datetime.utcnow(),
    }
    await db.users.insert_one(demo_user)
    print(f"   Email: demo@teatree.org  |  Password: demo123")

    # Generate trees
    print("🌳 Generating 300 tea tree records...")
    trees = generate_trees(300)
    await db.trees.insert_many(trees)
    print(f"   Inserted {len(trees)} trees across {len(LOCATIONS)} locations")

    # Generate environmental data
    print("🌡️  Generating environmental records...")
    env_records = generate_environmental_data(trees)
    await db.environmental_data.insert_many(env_records)
    print(f"   Inserted {len(env_records)} environmental records")

    # Create indexes
    print("📇 Creating indexes...")
    await db.users.create_index("email", unique=True)
    await db.trees.create_index("tree_id", unique=True)
    await db.trees.create_index([("latitude", 1), ("longitude", 1)])
    await db.trees.create_index("elevation")
    await db.trees.create_index("location_name")
    await db.environmental_data.create_index("tree_id")
    await db.environmental_data.create_index("timestamp")

    print("\n✅ Seed complete!")
    print(f"   Trees: {len(trees)}")
    print(f"   Environmental records: {len(env_records)}")
    print(f"   Demo login: demo@teatree.org / demo123")

    client.close()


if __name__ == "__main__":
    asyncio.run(seed())
