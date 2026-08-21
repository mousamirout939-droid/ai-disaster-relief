"""CLI wrapper to run the index-creation migration directly."""
import asyncio
import importlib

if __name__ == "__main__":
    migration = importlib.import_module("migrations.001_create_indexes")
    asyncio.run(migration.run())
