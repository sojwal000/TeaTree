"""
Tea Tree Lifecycle Intelligence Routes

Features:
1. Medicinal / bioactive information
2. Post-death biomass utilisation
3. Tea tree mortality risk assessment
"""

from datetime import datetime
from fastapi import APIRouter, HTTPException

from backend.database import get_database
from backend.services.mortality_service import (
    calculate_mortality_risk
)


router = APIRouter(
    prefix="/api/lifecycle",
    tags=["Tea Tree Lifecycle Intelligence"]
)


# ============================================================
# MEDICINAL / BIOACTIVE KNOWLEDGE
# ============================================================

MEDICINAL_PROFILE = {

    "scientific_name": "Camellia sinensis",

    "title": "Tea Plant Bioactive & Medicinal Research Profile",

    "description":
        "Camellia sinensis contains several biologically active "
        "compounds studied for potential health-related effects.",

    "plant_parts": [

        {
            "part": "Leaves",
            "importance": "Primary researched part",
            "compounds": [
                "Catechins",
                "EGCG",
                "Polyphenols",
                "Caffeine",
                "L-theanine"
            ],
            "research_areas": [
                "Antioxidant activity",
                "Cardiovascular research",
                "Metabolic health research",
                "Cognitive alertness"
            ]
        },

        {
            "part": "Young shoots",
            "importance": "Used for tea production",
            "compounds": [
                "Polyphenols",
                "Catechins",
                "Caffeine",
                "Amino acids"
            ],
            "research_areas": [
                "Functional beverages",
                "Bioactive compound extraction"
            ]
        },

        {
            "part": "Seeds",
            "importance": "Secondary research resource",
            "compounds": [
                "Seed oil",
                "Saponins"
            ],
            "research_areas": [
                "Industrial research",
                "Natural product research"
            ]
        }

    ],

    "major_compounds": [

        {
            "name": "EGCG",
            "full_name":
                "Epigallocatechin-3-gallate",
            "category": "Catechin",
            "research_interest":
                "Antioxidant and other biological activities"
        },

        {
            "name": "L-Theanine",
            "category": "Amino acid",
            "research_interest":
                "Cognition, attention and relaxation research"
        },

        {
            "name": "Caffeine",
            "category": "Alkaloid",
            "research_interest":
                "Central nervous system stimulation and alertness"
        },

        {
            "name": "Tea Polyphenols",
            "category": "Polyphenols",
            "research_interest":
                "Antioxidant, metabolic and cardiovascular research"
        }

    ],

    "evidence_notice":
        "This module presents research information and does not "
        "provide medical diagnosis, treatment or dosage advice."
}


# ============================================================
# POST-DEATH USE PROFILE
# ============================================================

POST_DEATH_PROFILE = {

    "title":
        "Tea Tree End-of-Life Biomass Utilisation",

    "description":
        "After a tea plant is confirmed dead or removed, its "
        "biomass may still have potential research or resource value.",

    "uses": [

        {
            "name": "Biochar",
            "material": [
                "Woody branches",
                "Pruning biomass"
            ],
            "description":
                "Tea biomass can be thermally converted into "
                "biochar for research into soil amendment and "
                "biomass recycling.",
            "priority": "High"
        },

        {
            "name": "Composting / Organic Matter",
            "material": [
                "Leaves",
                "Small branches",
                "Suitable plant residues"
            ],
            "description":
                "Suitable uncontaminated biomass may be evaluated "
                "for controlled composting or organic matter recycling.",
            "priority": "Medium"
        },

        {
            "name": "Biomass Research",
            "material": [
                "Stem",
                "Branches",
                "Roots"
            ],
            "description":
                "Dead biomass can be recorded for biomass quantity, "
                "carbon and decomposition research.",
            "priority": "Medium"
        },

        {
            "name": "Scientific Sample",
            "material": [
                "Stem cross-section",
                "Roots",
                "Leaves"
            ],
            "description":
                "Samples may be preserved for ring analysis, disease "
                "investigation, morphology or conservation research.",
            "priority": "High"
        },

        {
            "name": "Carbon / Circular-Economy Record",
            "material": [
                "Whole plant biomass"
            ],
            "description":
                "The platform can document how removed biomass is "
                "reused instead of treating the tree record as deleted.",
            "priority": "High"
        }

    ],

    "safety_notice":
        "Biomass suspected of carrying serious disease or contamination "
        "should not automatically be recommended for composting or reuse. "
        "A field specialist should determine appropriate disposal."
}


# ============================================================
# GET MEDICINAL PROFILE
# ============================================================

@router.get("/medicinal")
async def medicinal_profile():

    return MEDICINAL_PROFILE


@router.get("/medicinal/{tree_id}")
async def medicinal_profile_for_tree(
    tree_id: str
):

    db = get_database()

    tree = await db.trees.find_one(
        {"tree_id": tree_id},
        {"_id": 0}
    )

    if not tree:

        raise HTTPException(
            status_code=404,
            detail="Tree not found"
        )

    return {
        "tree_id": tree_id,
        "location_name":
            tree.get("location_name"),
        "scientific_name":
            "Camellia sinensis",
        "profile":
            MEDICINAL_PROFILE
    }


# ============================================================
# POST-DEATH USE
# ============================================================

@router.get("/post-death")
async def post_death_profile():

    return POST_DEATH_PROFILE


@router.get("/post-death/{tree_id}")
async def post_death_profile_for_tree(
    tree_id: str
):

    db = get_database()

    tree = await db.trees.find_one(
        {"tree_id": tree_id},
        {"_id": 0}
    )

    if not tree:

        raise HTTPException(
            status_code=404,
            detail="Tree not found"
        )

    return {
        "tree_id": tree_id,

        "location_name":
            tree.get("location_name"),

        "estimated_age":
            tree.get("ring_count"),

        "diameter":
            tree.get("diameter"),

        "height":
            tree.get("height"),

        "profile":
            POST_DEATH_PROFILE
    }


# ============================================================
# MORTALITY RISK
# ============================================================

@router.get("/mortality-risk/{tree_id}")
async def mortality_risk(
    tree_id: str
):

    db = get_database()

    tree = await db.trees.find_one(
        {"tree_id": tree_id},
        {"_id": 0}
    )

    if not tree:

        raise HTTPException(
            status_code=404,
            detail="Tree not found"
        )

    # --------------------------------------------------------
    # Latest environmental record
    # --------------------------------------------------------

    latest_environment = await db.environmental_data.find_one(
        {"tree_id": tree_id},
        {"_id": 0},
        sort=[("timestamp", -1)]
    )

    # --------------------------------------------------------
    # Health history
    # --------------------------------------------------------

    health_history = await (
        db.health_checks
        .find(
            {"tree_id": tree_id},
            {"_id": 0}
        )
        .sort("created_at", -1)
        .limit(20)
        .to_list(length=20)
    )

    # Different project versions may use health_history.
    if not health_history:

        health_history = await (
            db.health_history
            .find(
                {"tree_id": tree_id},
                {"_id": 0}
            )
            .sort("created_at", -1)
            .limit(20)
            .to_list(length=20)
        )

    # --------------------------------------------------------
    # Find EHI if stored/calculated previously
    # --------------------------------------------------------

    ecosystem_health_index = None

    ecosystem_record = await db.ecosystem_health.find_one(
        {"tree_id": tree_id},
        {"_id": 0},
        sort=[("created_at", -1)]
    )

    if ecosystem_record:

        ecosystem_health_index = (
            ecosystem_record.get(
                "ecosystem_health_index"
            )
            or ecosystem_record.get("ehi")
        )

    # --------------------------------------------------------
    # Calculate risk
    # --------------------------------------------------------

    result = calculate_mortality_risk(
        tree=tree,
        latest_environment=latest_environment,
        health_history=health_history,
        ecosystem_health_index=
            ecosystem_health_index
    )

    return result


# ============================================================
# ALL TREE RISKS
# ============================================================

@router.get("/mortality-risk")
async def all_mortality_risks():

    db = get_database()

    trees = await db.trees.find(
        {},
        {"_id": 0}
    ).to_list(length=2000)

    results = []

    for tree in trees:

        tree_id = tree["tree_id"]

        env = await db.environmental_data.find_one(
            {"tree_id": tree_id},
            {"_id": 0},
            sort=[("timestamp", -1)]
        )

        history = await (
            db.health_checks
            .find(
                {"tree_id": tree_id},
                {"_id": 0}
            )
            .sort("created_at", -1)
            .limit(10)
            .to_list(length=10)
        )

        result = calculate_mortality_risk(
            tree,
            env,
            history,
            None
        )

        result["location_name"] = (
            tree.get("location_name")
        )

        results.append(result)

    results.sort(
        key=lambda item:
            item["mortality_risk_score"],
        reverse=True
    )

    return {
        "total": len(results),
        "trees": results
    }


# ============================================================
# CONFIRM TREE DEATH
# ============================================================

@router.post("/death/{tree_id}")
async def record_tree_death(
    tree_id: str
):

    db = get_database()

    tree = await db.trees.find_one(
        {"tree_id": tree_id},
        {"_id": 0}
    )

    if not tree:

        raise HTTPException(
            status_code=404,
            detail="Tree not found"
        )

    now = datetime.utcnow()

    death_record = {

        "tree_id": tree_id,

        "location_name":
            tree.get("location_name"),

        "confirmed_dead": True,

        "confirmed_at": now,

        "height":
            tree.get("height"),

        "diameter":
            tree.get("diameter"),

        "ring_count":
            tree.get("ring_count"),

        "latitude":
            tree.get("latitude"),

        "longitude":
            tree.get("longitude"),

        "post_death_options":
            POST_DEATH_PROFILE["uses"]
    }

    await db.tree_death_records.update_one(
        {"tree_id": tree_id},
        {"$set": death_record},
        upsert=True
    )

    await db.trees.update_one(
        {"tree_id": tree_id},
        {
            "$set": {
                "life_status": "dead",
                "death_confirmed_at": now,
                "updated_at": now
            }
        }
    )

    return {
        "message":
            "Tree death recorded successfully.",

        "tree_id":
            tree_id,

        "life_status":
            "dead",

        "post_death_options":
            POST_DEATH_PROFILE["uses"]
    }