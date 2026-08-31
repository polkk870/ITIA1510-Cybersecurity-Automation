# Ask the user for account information and the password to analyze
account = input("Enter the account name: ")
username = input("Enter the username: ")
password = input("Enter the password to analyze: ")
rotation_interval = input("Enter the rotation interval in months: ")

# Convert rotation interval from text to an integer so we can do math with it
rotation_interval = int(rotation_interval)

# REQUIRED CALCULATIONS
# Count how many characters are in the password
password_length = len(password)

length_score = password_length * 10

# Calculate how many rotations happen in 36 months (3 years)
rotation_count = 36 // rotation_interval

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

