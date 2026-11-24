"""Lab 6 - Branch coverage tests for car_insurance_premium.py

Every decision is tested for both its True and False outcome,
including boundary values (17/18, 24/25, 59/60, claims 0/1/2/3, ...).
"""
import pytest
from car_insurance_premium import annual_premium, no_claim_bonus, claim_payout


# ---------- annual_premium: validation branches ----------
def test_sedan_no_claims():
    assert annual_premium("sedan", 30, 0, False) == 9600


@pytest.mark.parametrize("car", ["truck", "", "SEDAN"])
def test_unknown_car_type(car):
    with pytest.raises(ValueError, match="unknown car type"):
        annual_premium(car, 30, 0, False)


def test_driver_age_17_rejected():
    with pytest.raises(ValueError, match="driver too young"):
        annual_premium("sedan", 17, 0, False)


def test_driver_age_18_accepted():
    # 18 is the minimum valid age: 12000 + 4000 = 16000, -20% = 12800
    assert annual_premium("sedan", 18, 0, False) == 12800


# ---------- annual_premium: age branches ----------
def test_age_24_young_surcharge():
    # 8000 + 4000 = 12000, 1 claim -> unchanged
    assert annual_premium("hatchback", 24, 1, False) == 12000


def test_age_25_no_surcharge():
    # boundary: 25 is NOT young and NOT senior
    assert annual_premium("hatchback", 25, 1, False) == 8000


def test_age_59_no_surcharge():
    assert annual_premium("hatchback", 59, 1, False) == 8000


def test_age_60_senior_surcharge():
    # 8000 + 2000 = 10000
    assert annual_premium("hatchback", 60, 1, False) == 10000


# ---------- annual_premium: claims branches ----------
def test_zero_claims_discount():
    # 15000 - 3000 = 12000
    assert annual_premium("suv", 30, 0, False) == 12000


def test_one_claim_no_change():
    assert annual_premium("suv", 30, 1, False) == 15000


def test_two_claims_no_change():
    # boundary: 2 claims is NOT more than 2
    assert annual_premium("suv", 30, 2, False) == 15000


def test_three_claims_doubled():
    assert annual_premium("suv", 30, 3, False) == 30000


# ---------- annual_premium: anti-theft branches ----------
def test_anti_theft_true():
    assert annual_premium("suv", 30, 1, True) == 14500


def test_anti_theft_false():
    assert annual_premium("suv", 30, 1, False) == 15000


def test_all_surcharges_combined():
    # hatchback, age 20: 12000; 0 claims: -2400 = 9600; anti-theft: 9100
    assert annual_premium("hatchback", 20, 0, True) == 9100


# ---------- no_claim_bonus ----------
def test_no_bonus():
    assert no_claim_bonus(0) == 0


def test_bonus_negative_years():
    with pytest.raises(ValueError, match="invalid years"):
        no_claim_bonus(-1)


@pytest.mark.parametrize("years, expected", [
    (1, 20), (2, 20),        # >= 1 and < 3
    (3, 35), (4, 35),        # >= 3 and < 5
    (5, 50), (10, 50),       # >= 5
])
def test_bonus_tiers(years, expected):
    assert no_claim_bonus(years) == expected


# ---------- claim_payout ----------
def test_payout_negative_damage():
    with pytest.raises(ValueError, match="invalid amount"):
        claim_payout(-1, 50000, 1000, False)


def test_payout_negative_deductible():
    with pytest.raises(ValueError, match="invalid amount"):
        claim_payout(1000, 50000, -1, False)


def test_payout_total_loss():
    assert claim_payout(80000, 60000, 1000, True) == 60000


def test_payout_damage_equals_deductible():
    # boundary: damage == deductible -> 0
    assert claim_payout(1000, 50000, 1000, False) == 0


def test_payout_damage_below_deductible():
    assert claim_payout(500, 50000, 1000, False) == 0


def test_payout_normal():
    assert claim_payout(10000, 50000, 1000, False) == 9000


def test_payout_equals_insured_value():
    # boundary: payout == insured_value is NOT capped, same result
    assert claim_payout(51000, 50000, 1000, False) == 50000


def test_payout_capped_at_insured_value():
    assert claim_payout(70000, 50000, 1000, False) == 50000
