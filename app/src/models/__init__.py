from .base import Base

# from .full_spoorkabel import FullSpoorkabel
from .group_membership_relation import GroupMembershipRelation
from .group_model import Group
from .group_project_relation import GroupProjectRelation
from .location_model import Location
from .organization_member_model import OrganizationMember
from .organization_model import Organization
from .project_model import Project
from .prorail_gil_model import ProrailGil
from .spoorkabel_model import Spoorkabel
from .spoorkabel_prorail_relation import SpoorkabelProrailRelation
from .spoorkabel_versie_relation import SpoorkabelVersieDetail
from .tekening_model import Tekening
from .upload_model import Upload
from .user_login_model import UserLogin
from .user_model import User
from .user_settings_model import UserSettings
from .versie_model import Versie, VersieBestaand, VersieOntwerp, VersieOntwerpFase

CORE_MODELS = [
    "Base",
    "GroupMembershipRelation",
    "Group",
    "GroupProjectRelation",
    "Location",
    "ProrailGil",
    "Spoorkabel",
    "SpoorkabelProrailRelation",
    "SpoorkabelProrailRelation",
    "SpoorkabelVersieDetail",
    "Tekening",
    "Upload",
    "User",
    "UserLogin",
    "UserSettings",
]

VERSIE_MODELS = ["Versie", "VersieBestaand", "VersieOntwerp", "VersieOntwerpFase"]

ORGANIZATION_MODELS = ["Organization", "OrganizationMember"]

__all__ = CORE_MODELS + VERSIE_MODELS + ORGANIZATION_MODELS
