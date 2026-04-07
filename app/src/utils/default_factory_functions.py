import re
import uuid
from datetime import datetime, timezone


def get_uuid_prefix() -> str:
    full_uuid = str(uuid.uuid4())
    return full_uuid.split("-")[0]


def utc_now_ms() -> int:
    return int(datetime.now(timezone.utc).timestamp() * 1000)


def get_discipline_from_tekeningnaam(tekeningnaam: str) -> str:
    match = re.search(r"KS|WB|WV|RD", tekeningnaam)

    if not match:
        raise ValueError("Could not find discipline in tekeningnaam (KS, WB, RD or WV)")

    return match.group(0)