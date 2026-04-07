import sys
from os import path

from alembic import context

# 1. ADD THIS: Let Alembic find your 'src' folder
# Since env.py is in app/migrations/, we go up two levels to find 'src'
sys.path.append(path.join(path.dirname(__file__), "..", "src"))


# 2. IMPORT your stuff from your app
from core.database import DATABASE_URL
from models.base import Base

# from models.other_model import Other

# 3. SET target_metadata
target_metadata = Base.metadata

# 4. (Optional) Inject your DB URL from your Python config instead of alembic.ini
config = context.config
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# ... (keep the rest of the generated file as is)
