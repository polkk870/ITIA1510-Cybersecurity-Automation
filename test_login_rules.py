from login_rules import is_locked_out, session_expired, risk_level

# is_locked_out tests

assert is_locked_out(4, 5) == False
print("PASS: is_locked_out correctly returned False for 4 attempts with limit 5")

assert is_locked_out(5, 5) == True
print("PASS: is_locked_out correctly returned True for 5 attempts with limit 5")

# session_expired tests

assert session_expired(9, 10) == False
print("PASS: session_expired correctly returned False for 9 idle minutes with timeout 10")

assert session_expired(11, 10) == True
print("PASS: session_expired correctly returned True for 11 idle minutes with timeout 10")

# risk_level tests

assert risk_level(2) == "LOW"
print("PASS: risk_level correctly returned LOW for 2 attempts")

assert risk_level(3) == "MEDIUM"
print("PASS: risk_level correctly returned MEDIUM for 3 attempts")

assert risk_level(6) == "HIGH"
print("PASS: risk_level correctly returned HIGH for 6 attempts")

print("----------------------------------------")
print("All tests passed.")
