import pytest
from password_checker import (
    check_length,
    check_digit,
    check_username,
    check_rotation,
    check_breach,
    known_breached,
    policy
)

# -----------------------------
# check_length tests
# -----------------------------

def test_length_short():
    ok, verdict = check_length("abcd", policy)
    assert ok is False

def test_length_minimum():
    ok, verdict = check_length("abcdefgh", policy)
    assert ok is True

def test_length_strong():
    ok, verdict = check_length("abcdefghijklmnop", policy)
    assert ok is True
    assert verdict.lower().startswith("password length strong")

# -----------------------------
# check_digit tests
# -----------------------------

def test_digit_not_found():
    assert check_digit("password") is False

def test_digit_found():
    assert check_digit("passw0rd") is True

# -----------------------------
# check_username tests
# -----------------------------

def test_username_match():
    assert check_username("katelyn", "katelyn") is False

def test_username_not_match():
    assert check_username("securepass", "katelyn") is True

# -----------------------------
# check_rotation tests
# -----------------------------

def test_rotation_too_long():
    ok, verdict = check_rotation(18, policy)
    assert ok is False

def test_rotation_good():
    ok, verdict = check_rotation(6, policy)
    assert ok is True

# -----------------------------
# check_breach tests
# -----------------------------

def test_breach_found():
    assert check_breach("password123", known_breached) is False

def test_breach_not_found():
    assert check_breach("MySecurePass!2024", known_breached) is True

# -----------------------------
# Week 06 policy dictionary tests
# -----------------------------

def test_policy_strong_length():
    assert policy["strong_length"] == 15

def test_policy_has_require_digit():
    assert "require_digit" in policy

def test_policy_min_length():
    assert policy["min_length"] == 8

# -----------------------------
# Additional safety tests
# -----------------------------

def test_breach_list_exists():
    assert isinstance(known_breached, list)
    assert len(known_breached) > 0

def test_policy_is_dict():
    assert isinstance(policy, dict)

