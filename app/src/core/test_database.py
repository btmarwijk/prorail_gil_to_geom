"""
Run this once to create all tables and confirm they landed correctly.

    python test_models.py
"""

from core.database import engine, init_db
from models import (
    Group,
    GroupMembershipRelation,
    GroupProjectRelation,
    Location,
    Project,
    ProrailGil,
    Spoorkabel,
    SpoorkabelProrailRelation,
    SpoorkabelVersieDetail,
    Tekening,
    Upload,
    User,
    UserLogin,
    UserSettings,
    Versie,
    VersieBestaand,
    VersieOntwerp,
    VersieOntwerpFase,
)
from sqlalchemy import inspect, text

EXPECTED_TABLES = {
    "groups": Group,
    "group_members": GroupMembershipRelation,
    "group_project_relations": GroupProjectRelation,
    "locations": Location,
    "projecten": Project,
    "prorail_gil": ProrailGil,
    "spoorkabel": Spoorkabel,
    "spoorkabel_prorail_feature_relation": SpoorkabelProrailRelation,
    "kabel_versie_details": SpoorkabelVersieDetail,
    "tekeningen": Tekening,
    "upload": Upload,
    "user": User,
    "user_logins": UserLogin,
    "user_settings": UserSettings,
    "versies": Versie,
    "versie_bestaand": VersieBestaand,
    "versie_ontwerp": VersieOntwerp,
    "versie_ontwerp_fase": VersieOntwerpFase,
}


def check_postgis(conn):
    result = conn.execute(
        text("SELECT extversion FROM pg_extension WHERE extname = 'postgis'")
    ).fetchone()
    if result:
        print(f"  postgis {result[0]}")
    else:
        print("  postgis NOT found — geometry columns will fail")


def check_tables(inspector):
    existing = set(inspector.get_table_names())
    print(f"\n{'Table':<45} {'Status':<10} {'Columns'}")
    print("-" * 100)
    all_ok = True
    for table_name, model_class in EXPECTED_TABLES.items():
        if table_name in existing:
            cols = [c["name"] for c in inspector.get_columns(table_name)]
            print(f"  {table_name:<43} {'OK':<10} {', '.join(cols)}")
        else:
            print(f"  {table_name:<43} {'MISSING':<10}")
            all_ok = False
    return all_ok


def check_foreign_keys(inspector):
    print(f"\n{'Table':<45} Foreign keys")
    print("-" * 100)
    for table_name in EXPECTED_TABLES:
        fks = inspector.get_foreign_keys(table_name)
        if fks:
            for fk in fks:
                ref = f"{fk['referred_table']}.{fk['referred_columns'][0]}"
                local = fk["constrained_columns"][0]
                print(f"  {table_name:<43} {local} → {ref}")


def check_geometry_columns(conn):
    result = conn.execute(
        text("""
            SELECT f_table_name, f_geometry_column, srid, type
            FROM geometry_columns
            WHERE f_table_name = ANY(:tables)
            ORDER BY f_table_name
        """),
        {
            "tables": [
                "spoorkabel",
                "kabel_versie_details",
                "full_spoorkabel",
                "prorail_gil",
            ]
        },
    ).fetchall()
    print(f"\n{'Table':<45} {'Column':<20} {'SRID':<8} Type")
    print("-" * 100)
    for row in result:
        print(f"  {row[0]:<43} {row[1]:<20} {row[2]:<8} {row[3]}")


if __name__ == "__main__":
    print("=== 1. Creating extension + tables ===")
    init_db()
    print("  done\n")

    inspector = inspect(engine)

    print("=== 2. PostGIS extension ===")
    with engine.connect() as conn:
        check_postgis(conn)

    print("\n=== 3. Tables + columns ===")
    all_ok = check_tables(inspector)

    print("\n=== 4. Foreign keys ===")
    check_foreign_keys(inspector)

    print("\n=== 5. Geometry columns ===")
    with engine.connect() as conn:
        check_geometry_columns(conn)

    print("\n=== Result ===")
    if all_ok:
        print("  All tables present.")
    else:
        print("  Some tables are missing — check errors above.")
