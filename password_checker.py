account = input("Enter the account name: ")
username = input("Enter the username: ")
password = input("Enter the password to analyze: ")
rotation_interval = input("Enter the rotation interval in months: ")

rotation_interval = int(rotation_interval)

# REQUIRED CALCULATIONS
password_length = len(password)
length_score = password_length * 10
rotation_count = 36 // rotation_interval

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

