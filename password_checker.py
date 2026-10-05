# policy is defined at module level so every function can read the same rules.
# placing it here means changing a rule only requires editing one line.
policy = {
    "min_length": 8,
    "strong_length": 15,
    "max_rotation_months": 12,
    "good_rotation_months": 6,
    "require_digit": True,
    "check_breach_list": True
}

def check_length(password, policy):
    """
    Checks password length against policy.
    Takes a password string.
    Returns (length_ok: bool, length_verdict: str).
    """
    password_length = len(password)

    # reading limits from policy avoids hard-coding numbers inside functions
    if password_length < policy["min_length"]:
        return False, "Password too short"
    elif password_length < policy["strong_length"]:
        return True, "Password length OK"
    else:
        return True, "Password length STRONG"


def check_digit(password):
    """
    Checks whether password contains at least one digit.
    Takes a password string.
    Returns has_digit: bool.
    """
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


def check_rotation(rotation_interval, policy):
    """
    Checks whether rotation interval meets policy.
    Takes rotation interval as an integer (months).
    Returns (rotation_ok: bool, rotation_verdict: str).
    """
    # reading limits from policy keeps rotation rules consistent everywhere
    if rotation_interval <= policy["good_rotation_months"]:
        return True, "Rotation interval ideal"
    elif rotation_interval <= policy["max_rotation_months"]:
        return True, "Rotation interval acceptable"
    else:
        return False, "Rotation interval too long"


known_breached = [
    "password", "password123", "123456", "qwerty", "letmein",
    "welcome", "monkey", "dragon", "master", "sunshine"
]

def check_breach(password, known_breached):
    """
    Returns True when password is NOT in the known breach list.
    """
    return password not in known_breached


def audit_password(account, username, password, rotation_interval, known_breached, policy):
    """
    Orchestrates all password checks and prints full report.
    Returns (passed, failed, critical) as integers (1 or 0).
    """

    length_ok, length_verdict = check_length(password, policy)
    has_digit = check_digit(password)
    not_username = check_username(password, username)
    rotation_ok, rotation_verdict = check_rotation(rotation_interval, policy)
    not_breached = check_breach(password, known_breached)

    print("\n========================================")
    print("   PASSWORD AUDIT REPORT")
    print("========================================")
    print(f"Account:           {account}")
    print(f"Username:          {username}")
    print(f"Password length:   {len(password)} characters")
    print(f"Length score:      {len(password) * 10} points")
    print(f"Rotation interval: {rotation_interval} months")
    print(f"Rotations (3 yr):  {36 // rotation_interval}")
    print("----------------------------------------")
    print(f"Length verdict:    {length_verdict}")
    print(f"Digit found:       {'YES' if has_digit else 'NO'}")
    print(f"Username match:    {'NO' if not_username else 'YES'}")
    print(f"Breach check:      {'OK' if not_breached else 'CRITICAL -- password found in known breach list'}")
    print(f"Rotation verdict:  {rotation_verdict}")
    print("----------------------------------------")

    passed = failed = 0

    if length_ok and has_digit and not_username and not_breached and rotation_ok:
        passed = 1
        print("OVERALL: PASS -- meets all requirements")
    else:
        failed = 1
        print("OVERALL: FAIL -- see findings above")

    # critical means username match OR breach list hit
    is_critical = (not not_username) or (not not_breached)

    return passed, failed, is_critical


if __name__ == '__main__':

    # credentials now stored as dictionaries so fields are reached by key
    credentials = [
        {"account": "Gmail", "username": "jsmith", "password": "password123", "rotation_interval": 12},
        {"account": "SSH Server", "username": "jsmith", "password": "jsmith", "rotation_interval": 24},
        {"account": "VPN", "username": "jsmith", "password": "Tr0ub4dor&3correct", "rotation_interval": 3},
        {"account": "Company Email", "username": "jsmith", "password": "summer2024!", "rotation_interval": 6},
        {"account": "GitHub", "username": "jsmith", "password": "Blue-Harbor-72-Lantern", "rotation_interval": 6}
    ]

    # summary dictionary replaces multiple counters
    summary = {
        "total": 0,
        "passed": 0,
        "failed": 0,
        "critical": 0,
        "failed_accounts": [],
        "critical_accounts": []
    }

    for cred in credentials:
        summary["total"] += 1

        passed, failed, critical = audit_password(
            cred["account"],
            cred["username"],
            cred["password"],
            cred["rotation_interval"],
            known_breached,
            policy
        )

        if passed:
            summary["passed"] += 1
        if failed:
            summary["failed"] += 1
            summary["failed_accounts"].append(cred["account"])
        if critical:
            summary["critical"] += 1
            summary["critical_accounts"].append(cred["account"])

    print("\n========================================")
    print("   BATCH AUDIT SUMMARY")
    print("========================================")
    print(f"Credentials audited: {summary.get('total', 0)}")
    print(f"Passed:              {summary.get('passed', 0)}")
    print(f"Failed:              {summary.get('failed', 0)}")
    print("----------------------------------------")
    print("Failed accounts:     " + ", ".join(summary.get("failed_accounts", [])))
    print(f"Critical flags:      {summary.get('critical', 0)}")
    print("Critical accounts:   " + ", ".join(summary.get("critical_accounts", [])))
    print("----------------------------------------")
    print("NOTE: Credentials and breach list are hardcoded -- file reading coming in Week 07.")
    print("========================================")

