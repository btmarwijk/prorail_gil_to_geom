def is_valid_excel(contents: bytes) -> bool:
    """
    Valideert of de bytes van een bestand overeenkomen met de
    bekende 'magic bytes' van Excel-formaten.
    """
    # Een leeg bestand of te klein bestand is sowieso ongeldig
    if len(contents) < 8:
        return False

    # 1. Moderne Excel bestanden (.xlsx, .xlsm)
    # Dit zijn technisch gezien ZIP-bestanden.
    # Magic bytes: 50 4B 03 04 (ASCII: PK..)
    if contents.startswith(b"PK\x03\x04"):
        return True

    # 2. Oude Excel bestanden (.xls / Excel 97-2003)
    # Dit is het OLE2 / Compound File Binary Format.
    # Magic bytes: D0 CF 11 E0 A1 B1 1A E1
    if contents.startswith(b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"):
        return True

    return False
