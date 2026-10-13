import json

# policy is defined at module level so every function reads the same rules.
# placing it here means changing a rule only requires editing one line.
policy = {
    "min_length": 8,
    "strong_length": 15,
    "max_rotation_months": 12,
    "good_rotation_months": 6,
    "require_digit": True,
    "check_breach_list": True
}

# ---------------------------------------------------------------------------
# FILE LOADING FUNCTIONS (Week 07)
# ---------------------------------------------------------------------------

def load_breached(filepath):
    """Read the breached password file. Returns a list of password strings."""
    known_breached = []
    # with closes the file automatically even if an error stops the program
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if line != "":          # skip blank lines so split() never breaks
                known_breached.append(line)
    return known_breached


def load_credentials(filepath):
    """Read credentials.txt and return a list of account dictionaries."""
    credentials = []
    # with ensures safe closing even if exceptions occur
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if line == "":          # skip blank lines so fields always exist
                continue
            fields = line.split(",")
            credentials.append({
                "account": fields[0],
                "username": fields[1],
                "password": fields[2],
                "rotation_interval": int(fields[3]),
            })
    return credentials


def write_report(report_lines, filepath):
    """Write each string in report_lines to the file as one line."""
    # write mode overwrites the file every run, which is fine for this lab
    with open(filepath, "w") as f:
        for line in report_lines:
            f.write(line + "\n")    # write() does NOT add newline automatically


# ---------------------------------------------------------------------------
# CHECK FUNCTIONS (unchanged from Week 06)
# ---------------------------------------------------------------------------

def check_length(password, policy):
    password_length = len(password)

    if password_length < policy["min_length"]:
        return False, "Password too short"
    elif password_length < policy["strong_length"]:
        return True, "Password length OK"
    else:
        return True, "Password length STRONG"


def check_digit(password):
    for char in password:
        if char.isdigit():
            return True
    return False


def check_username(password, username):
    return password != username


def check_rotation(rotation_interval, policy):
    if rotation_interval <= policy["good_rotation_months"]:
        return True, "Rotation interval ideal"
    elif rotation_interval <= policy["max_rotation_months"]:
        return True, "Rotation interval acceptable"
    else:
        return False, "Rotation interval too long"


def check_breach(password, known_breached):
    return password not in known_breached


# ---------------------------------------------------------------------------
# REPORT GENERATION (Week 07 changes)
# ---------------------------------------------------------------------------

def audit_password(account, username, password, rotation_interval, known_breached, policy, report_lines):
    """Runs all password checks and appends the full report to report_lines."""

    length_ok, length_verdict = check_length(password, policy)
    has_digit = check_digit(password)
    not_username = check_username(password, username)
    rotation_ok, rotation_verdict = check_rotation(rotation_interval, policy)
    not_breached = check_breach(password, known_breached)

    report_lines.append("========================================")
    report_lines.append("   PASSWORD AUDIT REPORT")
    report_lines.append("========================================")
    report_lines.append(f"Account:           {account}")
    report_lines.append(f"Username:          {username}")
    report_lines.append(f"Password length:   {len(password)} characters")
    report_lines.append(f"Length score:      {len(password) * 10} points")
    report_lines.append(f"Rotation interval: {rotation_interval} months")
    report_lines.append(f"Rotations (3 yr):  {36 // rotation_interval}")
    report_lines.append("----------------------------------------")
    report_lines.append(f"Length verdict:    {length_verdict}")
    report_lines.append(f"Digit found:       {'YES' if has_digit else 'NO'}")
    report_lines.append(f"Username match:    {'NO' if not_username else 'YES'}")
    report_lines.append(f"Breach check:      {'OK' if not_breached else 'CRITICAL -- password found in known breach list'}")
    report_lines.append(f"Rotation verdict:  {rotation_verdict}")
    report_lines.append("----------------------------------------")

    passed = failed = 0

    if length_ok and has_digit and not_username and not_breached and rotation_ok:
        passed = 1
        report_lines.append("OVERALL: PASS -- meets all requirements")
    else:
        failed = 1
        report_lines.append("OVERALL: FAIL -- see findings above")

    # critical means username match OR breach list hit
    is_critical = (not not_username) or (not not_breached)

    return passed, failed, is_critical


# ---------------------------------------------------------------------------
# MAIN PROGRAM (Week 07)
# ---------------------------------------------------------------------------

if __name__ == '__main__':

    credentials = load_credentials("credentials.txt")
    known_breached = load_breached("breached.txt")
    report_lines = []

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
            policy,
            report_lines
        )

        if passed:
            summary["passed"] += 1
        if failed:
            summary["failed"] += 1
            summary["failed_accounts"].append(cred["account"])
        if critical:
            summary["critical"] += 1
            summary["critical_accounts"].append(cred["account"])

    report_lines.append("========================================")
    report_lines.append("   BATCH AUDIT SUMMARY")
    report_lines.append("========================================")
    report_lines.append(f"Credentials audited: {summary['total']}")
    report_lines.append(f"Passed:              {summary['passed']}")
    report_lines.append(f"Failed:              {summary['failed']}")
    report_lines.append("----------------------------------------")
    report_lines.append("Failed accounts:     " + ", ".join(summary["failed_accounts"]))
    report_lines.append(f"Critical flags:      {summary['critical']}")
    report_lines.append("Critical accounts:   " + ", ".join(summary["critical_accounts"]))
    report_lines.append("========================================")

    # print to console
    for line in report_lines:
        print(line)

    # save to file
    write_report(report_lines, "report.txt")


