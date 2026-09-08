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
<<<<<<< HEAD
=======
=======
# -------------------------
# Week 02: Classification Layer
# -------------------------

# Classify password length
if password_length < 8:
    length_verdict = "WEAK -- does not meet minimum length requirements"
elif password_length <= 11:
    length_verdict = "MODERATE -- meets minimum but falls short of NIST recommendations"
elif password_length <= 14:
    length_verdict = "GOOD -- acceptable length for most systems"
else:
    length_verdict = "STRONG -- meets NIST SP 800-63B recommendations"

# Check for at least one digit
# Future weeks replace this long chain with any() and a loop
has_digit = ('0' in password or '1' in password or '2' in password or
             '3' in password or '4' in password or '5' in password or
             '6' in password or '7' in password or '8' in password or
             '9' in password)

# Username-as-password check
not_username = password != username
# If not_username is False, the password is dangerously identical to the username

# Rotation frequency classification
if rotation_interval > 12:
    rotation_verdict = "WARNING -- rotation interval exceeds recommended maximum of 12 months"
elif rotation_interval >= 6:
    rotation_verdict = "ACCEPTABLE -- rotation interval within recommended range"
else:
    rotation_verdict = "EXCELLENT -- frequent rotation policy detected"

# Overall verdict logic
length_ok = password_length >= 15
# overall_pass is True only when ALL three conditions are True:
# The password is long enough, contains a digit, and does not match the username
overall_pass = length_ok and has_digit and not_username

# -------------------------
# Report Output (Week 02)
# -------------------------

print("====================================")
print("        PASSWORD AUDIT REPORT")
print("====================================")
print(f"Account:              {account}")
print(f"Username:             {username}")
print(f"Password length:      {password_length} characters")
print(f"Length score:         {length_score} points")
print(f"Rotation interval:    {rotation_interval} months")
print(f"Rotations (3 yr):     {rotation_count}")
print("------------------------------------")
print(f"Length verdict:       {length_verdict}")
print(f"Digit found:          {'YES' if has_digit else 'NO'}")
print(f"Username match:       {'NO' if not_username else 'YES'}")
print(f"Rotation verdict:     {rotation_verdict}")
print("------------------------------------")

if overall_pass:
    print("OVERALL: PASS -- password meets all checked criteria")
else:
    print("OVERALL: FAIL -- see findings above")

print("====================================")

>>>>>>> 6293dd5337ea3fc196cfaf55ce59730fb878cb05
