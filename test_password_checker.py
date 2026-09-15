# test_password_checker.py

from password_checker import check_length, check_digit, check_username, check_rotation

# -------------------------
# check_length tests
# -------------------------

length_ok, verdict = check_length("abcd")
assert length_ok == False
print("PASS: check_length correctly identified weak password")

length_ok, verdict = check_length("abcdefghijklmnop")
assert length_ok == True
print("PASS: check_length correctly identified strong password")

# -------------------------
# check_digit tests
# -------------------------

assert check_digit("password") == False
print("PASS: check_digit correctly returned False for password with no digits")

assert check_digit("passw0rd") == True
print("PASS: check_digit correctly returned True for password containing a digit")

# -------------------------
# check_username tests
# -------------------------

assert check_username("katelyn", "katelyn") == False
print("PASS: check_username correctly returned False when password matches username")

assert check_username("securepass", "katelyn") == True
print("PASS: check_username correctly returned True when password differs from username")

# -------------------------
# check_rotation tests
# -------------------------

rotation_ok, verdict = check_rotation(18)
assert rotation_ok == False
print("PASS: check_rotation correctly returned False for 18-month interval")

rotation_ok, verdict = check_rotation(6)
assert rotation_ok == True
print("PASS: check_rotation correctly returned True for 6-month interval")

print("----------------------------------------")
print("All 8 tests passed.")
