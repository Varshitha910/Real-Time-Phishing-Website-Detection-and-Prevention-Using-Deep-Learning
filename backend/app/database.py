"""MongoDB connection helpers.

The app uses Motor for async MongoDB access. In early development, routes can
still run without MongoDB if the database is unavailable, but production should
fail fast and surface connection problems through monitoring.
"""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from backend.app.config import get_settings


class MongoConnection:
    """Small connection holder used by FastAPI startup and shutdown hooks."""

    client: AsyncIOMotorClient | None = None


mongo = MongoConnection()


async def connect_to_mongo() -> None:
    """Create the MongoDB client during application startup."""

    settings = get_settings()
    mongo.client = AsyncIOMotorClient(settings.mongo_uri)


async def close_mongo_connection() -> None:
    """Close the MongoDB client during application shutdown."""

    if mongo.client is not None:
        mongo.client.close()
        mongo.client = None


def get_database() -> AsyncIOMotorDatabase:
    """Return the configured MongoDB database.

    Raises:
        RuntimeError: If the app tries to access MongoDB before startup.
    """

    if mongo.client is None:
        raise RuntimeError("MongoDB client is not initialized.")

    settings = get_settings()
    return mongo.client[settings.mongo_database]

