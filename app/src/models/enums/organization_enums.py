from enums import StrEnum


class LicenseStatus(StrEnum):
    ACTIVE = "active"
    EXPIRED = "expired"
    CANCELED = "canceled"
    TRIAL = "trial"


class InvitationStatus(StrEnum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    EXPIRED = "expired"
    REVOKED = "revoked"


class PlanName(StrEnum):
    FREE = "free"
    STARTER = "starter"
    PRO = "pro"
    BUSINESS = "business"
    ENTERPRISE = "enterprise"


class JobState(StrEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class EmailStatus(StrEnum):
    QUEUED = "queued"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"
    BOUNCED = "bounced"


PLAN_LIMITS = {
    "free": {
        "max_projects": 1,
        "max_users": 1,
        "storage_limit_gb": 1,
        "can_use_audit_logs": False,
    },
    "pro": {
        "max_projects": 25,
        "max_users": 10,
        "storage_limit_gb": 20,
        "can_use_audit_logs": True,
    },
    "business": {
        "max_projects": 50,
        "max_users": 50,
        "storage_limit_gb": 100,
        "can_use_audit_logs": True,
    },
    "enterprise": {
        "max_projects": 999999,
        "max_users": 999999,
        "storage_limit_gb": 1000,
        "can_use_audit_logs": True,
    },
}
