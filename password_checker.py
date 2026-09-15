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


def audit_password(account, username, password, rotation_interval):
    """
    Orchestrates all password checks and prints full report.
    Returns (passed, failed, critical) as integers (1 or 0).
    """
    length_ok, length_verdict = check_length(password)
    has_digit = check_digit(password)
    not_username = check_username(password, username)
    rotation_ok, rotation_verdict = check_rotation(rotation_interval)

    print(f"\nAccount: {account}")
    print(f"Username: {username}")
    print(f"Password: {password}")
    print(f"Length Check: {length_verdict}")
    print(f"Digit Check: {'Has digit' if has_digit else 'No digit'}")
    print(f"Username Check: {'OK' if not_username else 'Matches username'}")
    print(f"Rotation Check: {rotation_verdict}")

    # Returning a tuple allows other modules to use these results later
    passed = failed = critical = 0

    if length_ok and has_digit and not_username and rotation_ok:
        passed = 1
        print("RESULT: PASS")
    elif not length_ok or not has_digit or not_username:
        failed = 1
        print("RESULT: FAIL")
    else:
        critical = 1
        print("RESULT: CRITICAL")

    return passed, failed, critical


# This guard prevents the input loop from running when imported by test_password_checker.py
if __name__ == '__main__':
    total_pass = 0
    total_fail = 0
    critical_count = 0

    while True:
        account = input("Enter account name (or 'q' to quit): ")
        if account.lower() == 'q':
            break

        username = input("Enter username: ")
        password = input("Enter password: ")
        rotation_interval = int(input("Enter rotation interval (months): "))

        p, f, c = audit_password(account, username, password, rotation_interval)
        total_pass += p
        total_fail += f
        critical_count += c

    print("\nBatch Summary")
    print(f"Passed: {total_pass}")
    print(f"Failed: {total_fail}")
    print(f"Critical: {critical_count}")
    print("NOTE: Review critical accounts immediately.")

