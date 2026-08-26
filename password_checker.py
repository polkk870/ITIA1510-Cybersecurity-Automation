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

# Print the formatted password audit report
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
print("NOTE: Classification requires conditionals -- coming in Week 02.")
print("====================================")
