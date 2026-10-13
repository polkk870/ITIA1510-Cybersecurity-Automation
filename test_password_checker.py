import os
from password_checker import (
    check_length, check_digit, check_username, check_rotation,
    check_breach, load_credentials, load_breached, write_report, policy
)

known_breached = load_breached("breached.txt")

def test_check_length_short():
    ok, verdict = check_length("abc", policy)
    assert ok is False
    assert verdict == "Password too short"

def test_check_length_ok():
    ok, verdict = check_length("abcdefgh", policy)
    assert ok is True
    assert verdict == "Password length OK"

def test_check_length_strong():
    ok, verdict = check_length("abcdefghijklmnop", policy)
    assert ok is True
    assert verdict == "Password length STRONG"

def test_check_digit_yes():
    assert check_digit("abc3") is True

def test_check_digit_no():
    assert check_digit("abcdef") is False

def test_check_username_match():
    assert check_username("jsmith", "jsmith") is False

def test_check_username_nomatch():
    assert check_username("summer2024!", "jsmith") is True

def test_check_rotation_good():
    ok, verdict = check_rotation(3, policy)
    assert ok is True
    assert verdict == "Rotation interval ideal"

def test_check_rotation_ok():
    ok, verdict = check_rotation(12, policy)
    assert ok is True
    assert verdict == "Rotation interval acceptable"

def test_check_rotation_bad():
    ok, verdict = check_rotation(24, policy)
    assert ok is False
    assert verdict == "Rotation interval too long"

def test_check_breach_safe():
    assert check_breach("notbreached", known_breached) is True

def test_check_breach_hit():
    assert check_breach("password123", known_breached) is False

def test_load_credentials_returns_list():
    creds = load_credentials("credentials.txt")
    assert type(creds) is list

def test_load_credentials_first_record_has_account():
    creds = load_credentials("credentials.txt")
    assert "account" in creds[0]

def test_load_breached_returns_list():
    breached = load_breached("breached.txt")
    assert type(breached) is list

def test_load_breached_contains_password123():
    breached = load_breached("breached.txt")
    assert "password123" in breached

def test_write_report_creates_file():
    lines = ["hello", "world"]
    write_report(lines, "test_report.txt")

    with open("test_report.txt") as f:
        text = f.read()

    assert text == "hello\nworld\n"

    os.remove("test_report.txt")


