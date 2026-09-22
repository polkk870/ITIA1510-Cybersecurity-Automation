# password_checker.py

def check_length(password):
    """
    Checks password length against policy.
    Takes a password string.
    Returns (length_ok: bool, length_verdict: str).
    """
    # Replace this with your Week 03 length rules if needed
    if len(password) < 8:
        return False, "Password too short"
    else:
        return True, "Password length OK"


def check_digit(password):
    """
    Checks whether password contains at least one digit.
    Takes a password string.
    Returns has_digit: bool.
    """
    # Using a manual loop because Week 03 required explicit iteration
    for char in password:
        if char.isdigit():
            return True
    return False


def check_username(password, username):
    """
    Ensures password does not match username.
    Takes password and username strings.
    Returns not_username: bool.
    """
    return password != username


def check_rotation(rotation_interval):
    """
    Checks whether rotation interval meets policy.
    Takes rotation interval as an integer (months).
    Returns (rotation_ok: bool, rotation_verdict: str).
    """
    # Replace with your Week 03 rotation rules if needed
    if rotation_interval <= 12:
        return True, "Rotation interval acceptable"
    else:
        return False, "Rotation interval too long"
    
# known_breached is defined at module level so tests and all functions can access it
known_breached = [
    "password", "password123", "123456", "qwerty", "letmein",
    "welcome", "monkey", "dragon", "master", "sunshine"
]
def check_breach(password, known_breached):
    """
    Returns True when password is NOT in the known breach list.
    """
# Using `in` checks the whole list at once instead of looping item by item
    not_breached = password not in known_breached
    return not_breached



def audit_password(account, username, password, rotation_interval, known_breached):
    """
    Orchestrates all password checks and prints full report.
    Returns (passed, failed, critical) as integers (1 or 0).
    """

    # Run all Week 04 checks
    length_ok, length_verdict = check_length(password)
    has_digit = check_digit(password)
    not_username = check_username(password, username)
    rotation_ok, rotation_verdict = check_rotation(rotation_interval)

    # Week 05 breach check
    # Using `in` checks the whole list at once instead of looping item by item
    not_breached = check_breach(password, known_breached)

    # Print report rows
    print(f"\nAccount: {account}")
    print(f"Username: {username}")
    print(f"Password: {password}")
    print(f"Length Check: {length_verdict}")
    print(f"Digit Check: {'Has digit' if has_digit else 'No digit'}")
    print(f"Username Check: {'OK' if not_username else 'Matches username'}")
    print(f"Rotation Check: {rotation_verdict}")
    print(f"Breach Check: {'OK' if not_breached else 'CRITICAL -- password found in known breach list'}")

    # Determine pass/fail
    passed = failed = 0

    # Week 05 adds not_breached to the pass criteria
    if length_ok and has_digit and not_username and not_breached and rotation_ok:
        passed = 1
        print("RESULT: PASS")
    else:
        failed = 1
        print("RESULT: FAIL")

    # ⭐ THIS IS WHERE THE CRITICAL LOGIC GOES ⭐
    # A password is critical if:
    # - it matches the username OR
    # - it appears in the breach list
    is_critical = (not not_username) or (not not_breached)

    # Return values for main program
    return passed, failed, is_critical
# This guard prevents code from running when imported by test_password_checker.py
if __name__ == '__main__':

    # Hardcoded credentials list for Week 05 (file reading comes in Week 08)
    credentials = [
        ["Gmail", "jsmith", "password123", 12],
        ["SSH Server", "jsmith", "jsmith", 24],
        ["VPN", "jsmith", "Tr0ub4dor&3correct", 3],
        ["Company Email", "jsmith", "summer2024!", 6],
        ["GitHub", "jsmith", "Blue-Harbor-72-Lantern", 6],
    ]

    failed_accounts = []
    critical_accounts = []

    # Loop through each credential record
    for record in credentials:
        account = record[0]
        username = record[1]
        password = record[2]
        rotation_interval = record[3]

        passed, failed, critical = audit_password(
            account, username, password, rotation_interval, known_breached
        )

        if failed:
            failed_accounts.append(account)

        if critical:
            critical_accounts.append(account)

    # Batch summary
    print("\n========================================")
    print("   BATCH AUDIT SUMMARY")
    print("========================================")
    print(f"Credentials audited: {len(credentials)}")
    print(f"Passed:              {len(credentials) - len(failed_accounts)}")
    print(f"Failed:              {len(failed_accounts)}")
    print("----------------------------------------")
    print("Failed accounts:     " + ", ".join(failed_accounts))
    print(f"Critical flags:      {len(critical_accounts)}")
    print("Critical accounts:   " + ", ".join(critical_accounts))
    print("----------------------------------------")
    print("NOTE: Breach list and credentials are hardcoded -- file reading coming in Week 08.")
    print("========================================")
