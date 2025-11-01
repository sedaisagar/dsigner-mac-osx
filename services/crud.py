from db import fetch_profiles, fetch_profile_by_id, insert_profile, update_profile, delete_profile
from .event_publisher import get_publisher

# This file can be used to define higher-level CRUD operations or business logic if needed.
# For now, it directly imports and uses the database functions from db.py.

# Initialize publisher
publisher = get_publisher()