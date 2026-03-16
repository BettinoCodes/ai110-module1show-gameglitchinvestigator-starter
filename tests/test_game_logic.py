from logic_utils import check_guess, get_range_for_difficulty, parse_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result, _ = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result, _ = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result, _ = check_guess(40, 50)
    assert result == "Too Low"

# --- Tests for the string-comparison hint bug ---
# The old code cast numbers to strings on even attempts, causing "9" > "10"
# to be True (lexicographic order), which gave the wrong hint direction.

def test_guess_too_low_catches_string_comparison_bug():
    # 9 < 10 numerically, so the hint must be "Too Low"
    # With the old string-cast bug, "9" > "10" is True, so it would wrongly
    # return "Too High" — this test catches that regression.
    result, _ = check_guess(9, 10)
    assert result == "Too Low"

def test_guess_too_high_single_vs_double_digit():
    # 20 > 9 numerically, so the hint must be "Too High"
    # String comparison "20" < "9" is True, so the bug would flip this to
    # "Too Low" — this test catches that regression.
    result, _ = check_guess(20, 9)
    assert result == "Too High"

def test_winning_guess_single_digit():
    # Winning on a single-digit number should still return "Win"
    result, _ = check_guess(7, 7)
    assert result == "Win"

# --- Tests for get_range_for_difficulty (difficulty range bug) ---
# The bug: New Game always called randint(1, 100) regardless of difficulty,
# and the info bar always displayed "1 to 100". The fix lives in
# get_range_for_difficulty returning the correct (low, high) per mode.

def test_easy_range():
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20

def test_normal_range():
    low, high = get_range_for_difficulty("Normal")
    assert low == 1
    assert high == 100

def test_hard_range():
    low, high = get_range_for_difficulty("Hard")
    assert low == 1
    assert high == 50

# --- Edge case input tests ---

def test_negative_number_rejected():
    # -5 is below the minimum of 1, should be rejected with an error
    ok, val, _ = parse_guess("-5", low=1, high=100)
    assert ok == False
    assert val is None

def test_decimal_truncates_to_int():
    # 3.7 silently becomes 3 — documents this truncation behavior explicitly
    ok, val, _ = parse_guess("3.7", low=1, high=100)
    assert ok == True
    assert val == 3

def test_extremely_large_number_rejected():
    # 999999999999 is way outside any difficulty range, should be rejected
    ok, val, _ = parse_guess("999999999999", low=1, high=100)
    assert ok == False
    assert val is None
