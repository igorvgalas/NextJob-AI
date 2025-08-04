import asyncio
import json
from app.models import Skill
# Import the sessionmaker from database.py
from app.database import AsyncSessionLocal


async def load_skills(json_path: str):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    skills = data.get("skills", [])
    async with AsyncSessionLocal() as session:  # Use the configured sessionmaker
        async with session.begin():
            for skill in skills:
                db_skill = Skill(id=skill["id"], name=skill["name"])
                await session.merge(db_skill)  # insert or update if exists
        print(f"✅ Imported {len(skills)} skills.")


if __name__ == "__main__":
    asyncio.run(load_skills("skills_only.json"))
