from enum import Enum


class SpoorkabelStatus(Enum):
    NIEUW = "Nieuw"
    ONGEWIJZIGD = "Ongewijzigd"
    GEWIJZIGD = "Gewijzigd"
    VERWIJDERD = "Verwijderd"


class Groep(Enum):
    TELECOM = "Telecom"
    ENERGIE = "Energie"
    BEVEILIGING = "Beveiliging"
    DERDEN = "Derden"
    RIOLERING = "Riolering"
    OVERIGE = "Overige"
    VERLATEN = "Verlaten"
    WATER = "Water"
    ANTI_ICING = "Anti-icing"
    WISSELVERWARMING = "Wisselverwarming"
    LEEG = ""


class Subgroep(Enum):
    # --- Telecom ---
    GLASVEZEL = "Glasvezel"
    INTERLOKALE_TELECOM = "Interlokale Telecom"
    INTERLOKALE_TELECOM_AFTAKKING = "Interlokale Telecom Aftakking"
    LOKALE_TELECOM = "Lokale Telecom"
    CENTRALE_AFSTANDSBEDIENING = "Centrale afstandsbediening"
    CENTRALE_TREIN_AANDUIDING = "Centrale trein aanduiding"
    GSM_R = "GSM-R"
    OMROEP = "Omroep"
    TELEFOON = "Telefoon"

    # --- Energie ---
    V150KV = "150kV Voeding"
    V25KV = "25kV Voeding"
    V23KV = "23kV Voeding"
    V18KV = "18kV Voeding"
    V15KV = "15kV Voeding"
    V13KV = "13kV Voeding"
    V10KV = "10kV Voeding"
    EDS_V23KV = "23kV Voeding t.b.v EDS"
    EDS_V13KV = "13kV Voeding t.b.v EDS"
    EDS_V10KV = "10kV Voeding t.b.v EDS"
    V1500V = "1500V Voeding"
    MINUS_KABELS = "minus kabels"
    V3KV = "3kV Voeding"
    BOVENLEIDINGSCHAKELAAR = "Bovenleidingschakelaar"
    VERLICHTING_VERWARMING = "Verlichting/Verwarming"
    KAST_KAST_VERBINDING = "Kast/Kast verbinding"
    AARDING = "Aarding"

    # --- Beveiliging ---
    INTERLOKALE_BLOKKABEL = "Interlokale Blokkabel"
    OVERWEG = "Overweg"
    SEIN = "Sein"
    LICHTBAKSEIN = "Lichtbaksein"
    SECTIE = "Sectie"
    WAARSCHUWINGSINSTALLATIE = "Waarschuwingsinstallatie"
    WISSEL = "Wissel"
    BRUGCONTACT = "Brugcontact"
    PLAATSELIJKE_BEDIENING = "Plaatselijke bediening/drukknop"
    ATB = "Automatische Trein Beïnvloeding"
    ERTMS = "ERTMS"
    RETOUR = "Retour"

    # --- Derden ---
    NS = "Nederlandse Spoorwegen"
    OVCP = "Openbaar Vervoer Chipkaart"
    NEDTRAIN = "NedTrain"
    INFRASPEED = "Infraspeed"
    RELINED = "ReliNed"
    TELE2 = "Tele2"
    T_MOBILE = "T-Mobile"
    BT = "British Telecom"
    KPN = "KPN"

    # --- Overige Kabelsituatie ---
    FAZ = "Facilitaire Zaken"
    QUOVADIS = "QuoVadis"
    TTI = "Tunnel Technische Installaties"

    # --- Wisselverwarming ---
    GLYCOL = "Glycol"
    CENTRALE_BUIS = "Centrale Buis"
    GASLEIDING = "Gasleiding"

    # --- Water ---
    DRINKWATER = "Drinkwater"
    PROCESWATER = "Proceswater"
    DROGE_BRANDLEIDING = "Droge brandleiding"
    NATTE_BRANDLEIDING = "Natte brandleiding"

    # --- Riool ---
    VUILWATER = "Vuilwater"
    HEMELWATER = "Hemelwater"
    PERSLEIDING = "Persleiding"
    DIESEL = "Diesel"

    # --- Generiek ---
    BEKEND = "Bekend"
    OVERIGE = "Overige"
    ONBEKEND = "Onbekend"
    DRAINAGE = "Drainage"
    ELEKTRA = "Elektra"
    LEEG = ""


class GILType(Enum):
    GEUL = "Geul"
    KOKERTRACE = "Kokertrace"
    WATERKRUISING = "Waterkruising"
    SPOORKRUISING = "Spoorkruising"
    WEGKRUISING = "Wegkruising"
    TIJDELIJKE_GEUL = "Tijdelijke Geul"


class GILDiscipline(Enum):
    KABEL_SITUATIE = "KS"
    RIOOLDRAINAGE = "RD"
    WISSELVERWARMING = "WV"
    WATERBRANDLEIDING = "WB"


class UserRole(str, Enum):
    # Ultimate access; can manage system settings and other administrators.
    SUPER_ADMIN = "super_admin"

    # High-level access; typically manages standard users, billing, and global content.
    ADMIN = "admin"

    # Elevated access; typically manages user-generated content, comments, and disputes.
    MODERATOR = "moderator"

    # Standard authenticated user with access to baseline features and their own data.
    USER = "user"

    # Unauthenticated or temporary user with highly restricted read-only access.
    GUEST = "guest"

    # Special role for internal automated processes, cron jobs, or API integrations.
    SYSTEM = "system"

    # Specific role for compliance, auditing, or support staff who need to see data but cannot modify it.
    READ_ONLY = "read_only"
