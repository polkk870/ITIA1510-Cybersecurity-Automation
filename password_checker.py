# Week 03 password checker
# This program now processes multiple passwords instead of just one.
# Everything from Week 02 is still here, but moved inside a loop so it repeats.

# These counters must be outside the loop.
# Reason: they track totals across ALL passwords. If they were inside the loop,
# they would reset every time and never accumulate.
total_pass = 0
total_fail = 0
critical_count = 0

# Hardcoded batch size for Week 03.
# "Hardcoded" means the value is typed directly into the program instead of
# coming from a file or user input.
batch_size = 3
count = 0

# This loop runs once per password. It stops when count reaches batch_size.
while count < batch_size:
    print("========================================")
    print(f"   PASSWORD AUDIT REPORT  ({count + 1} of {batch_size})")
    print("========================================")

    # All input is now inside the loop so the user is asked for each password.
    account = input("Enter the account name: ")
    username = input("Enter the username: ")
    password = input("Enter the password to analyze: ")
    rotation_interval = int(input("Enter the rotation interval in months: "))

    # --- Week 02 logic moved inside the loop ---

    # Count characters in the password
    password_length = len(password)

    # Length score is simple math: 10 points per character
    length_score = password_length * 10

    # How many rotations happen in 36 months (3 years)
    rotation_count = 36 // rotation_interval

    # Length verdict based on NIST guidelines
    if password_length >= 12:
        length_verdict = "STRONG -- meets NIST SP 800-63B recommendations"
    else:
        length_verdict = "WEAK -- does not meet NIST SP 800-63B recommendations"

    # Loop-based digit check
    has_digit = False
    for char in password:
        if char in "0123456789":
            has_digit = True

    digit_text = "YES" if has_digit else "NO"

    # Username match check (CRITICAL flag)
    username_match = (username == password)
    username_text = "YES" if username_match else "NO"

    # Rotation verdict based on how often the password is changed
    if rotation_interval <= 6:
        rotation_verdict = "EXCELLENT -- frequent rotation policy detected"
    else:
        rotation_verdict = "POOR -- rotation interval too long"

    # OVERALL verdict
    if length_verdict.startswith("STRONG") and has_digit and not username_match:
        overall = "PASS -- password meets all checked criteria"
        total_pass += 1
    else:
        overall = "FAIL -- password does not meet all checked criteria"
        total_fail += 1

    # Count CRITICAL username-match flags
    if username_match:
        critical_count += 1

    # Print the full report for this password
    print(f"Account:              {account}")
    print(f"Username:             {username}")
    print(f"Password length:      {password_length} characters")
    print(f"Length score:         {length_score} points")
    print(f"Rotation interval:    {rotation_interval} months")
    print(f"Rotations (3 yr):     {rotation_count}")
    print("----------------------------------------")
    print(f"Length verdict:       {length_verdict}")
    print(f"Digit found:          {digit_text}")
    print(f"Username match:       {username_text}")
    print(f"Rotation verdict:     {rotation_verdict}")
    print("----------------------------------------")
    print(f"OVERALL: {overall}")
    print("========================================")

    # Increase the loop counter so the loop eventually ends
    count += 1

# After the loop finishes, print the batch summary.
print("========================================")
print("   BATCH AUDIT SUMMARY")
print("========================================")
print(f"Passwords audited: {batch_size}")
print(f"Passed:            {total_pass}")
print(f"Failed:            {total_fail}")
print(f"Critical flags:    {critical_count}")
print("----------------------------------------")
print("NOTE: Input is still hardcoded -- file reading coming in Week 08.")
print("========================================")
