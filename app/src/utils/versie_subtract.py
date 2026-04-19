def decrement_string(s):
    """Decrement a string like a base-26 number (A, B, C... AA, AB...)"""
    s = list(s)  # Convert to list for mutability

    for i in range(len(s) - 1, -1, -1):  # Start from the rightmost character
        if s[i] > "A":
            s[i] = chr(ord(s[i]) - 1)
            break
        else:
            # s[i] is 'A', so borrow from the left
            s[i] = "Z"
    else:
        return "Z" * (len(s) - 1)

    return "".join(s)


if __name__ == "__main__":
    # Test it
    versie = "C"
    print(versie, "→", decrement_string(versie))  # C → B

    versie = "AC"
    print(versie, "→", decrement_string(versie))  # AC → AB

    versie = "AA"
    print(versie, "→", decrement_string(versie))  # AA → Z

    versie = "BA"
    print(versie, "→", decrement_string(versie))  # BA → AZ
