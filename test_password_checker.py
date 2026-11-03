import json
from password_checker import breach_verdicts
import os
from password_checker import (
    check_length, check_digit, check_username, check_rotation,
    check_breach, load_credentials, load_breached, write_report,
    save_summary, load_summary, policy,
    load_history, add_to_history, save_history
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

def test_save_and_load_summary():
    sample = {
        "total": 2,
        "passed": 1,
        "failed": 1,
        "critical": 1,
        "failed_accounts": ["Gmail"],
        "critical_accounts": ["Gmail"]
    }

    save_summary(sample, "test_summary.json")

    assert load_summary("test_summary.json") == sample

    print("PASS: save_summary and load_summary gave back the same dictionary")


def test_failed_accounts_is_list():
    sample = {
        "total": 2,
        "passed": 1,
        "failed": 1,
        "critical": 1,
        "failed_accounts": ["Gmail"],
        "critical_accounts": ["Gmail"]
    }

    save_summary(sample, "test_summary.json")

    loaded = load_summary("test_summary.json")

    assert isinstance(loaded["failed_accounts"], list)

    print("PASS: failed_accounts remained a list")


def test_no_passwords_saved_in_json():
    sample = {
        "total": 2,
        "passed": 1,
        "failed": 1,
        "critical": 1,
        "failed_accounts": ["Gmail"],
        "critical_accounts": ["Gmail"]
    }

    save_summary(sample, "test_summary.json")

    with open("test_summary.json", "r") as f:
        contents = f.read()

    with open("credentials.txt", "r") as f:
        for line in f:
            parts = line.strip().split(",")

            if len(parts) == 4:
                password = parts[2]
                assert password not in contents

    print("PASS: no passwords appeared in saved JSON")


def test_load_history_missing_file():
    assert load_history("does_not_exist.json") == []

    print("PASS: load_history returns empty list for missing file")

def test_add_to_history_first_run():
    sample = {
        "passed": 2,
        "failed": 3,
        "critical_accounts": ["Gmail"]
    }

    history = add_to_history([], sample, 3)

    assert history[0]["run"] == 1

    print("PASS: first history entry is run 1")


def test_add_to_history_trim():
    sample = {
        "passed": 2,
        "failed": 3,
        "critical_accounts": ["Gmail"]
    }

    history = []

    for i in range(3):
        history = add_to_history(history, sample, 2)

    assert [entry["run"] for entry in history] == [2, 3]

    print("PASS: add_to_history kept only newest 2 runs")


def test_save_and_load_history():
    sample_history = [
        {
            "run": 1,
            "passed": 2,
            "failed": 3,
            "critical_accounts": ["Gmail"]
        }
    ]

    save_history(sample_history, "test_history.json")

    loaded = load_history("test_history.json")

    assert loaded == sample_history

    os.remove("test_history.json")

    print("PASS: save_history and load_history match")

def test_breach_verdicts_jsmith():
    known_breached = load_breached("breached.txt")

    result = breach_verdicts(
        "jsmith",
        load_credentials("credentials.txt"),
        known_breached
    )

    assert result["accounts"][0] == {
        "account": "Gmail",
        "on_breach_list": True
    }

    print("PASS: breach_verdicts marked the Gmail password as on the breach list")
    
def test_breach_verdicts_no_accounts():
    known_breached = load_breached("breached.txt")

    result = breach_verdicts(
        "nobody",
        load_credentials("credentials.txt"),
        known_breached
    )

    assert result["accounts"] == []

    print("PASS: breach_verdicts returned an empty list for a user with no accounts")

def test_breach_verdicts_no_passwords_exposed():
    known_breached = load_breached("breached.txt")

    result = breach_verdicts(
        "jsmith",
        load_credentials("credentials.txt"),
        known_breached
    )

    result_json = json.dumps(result)

    credentials = load_credentials("credentials.txt")

    for credential in credentials:

        # Skip SSH Server because its password is the same as the username.
        if credential["account"] == "SSH Server":
            continue

        assert credential["password"] not in result_json

    print("PASS: breach_verdicts does not expose passwords")