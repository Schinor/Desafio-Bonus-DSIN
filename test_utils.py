from Desafio_Bonus import utils as u


def test_feet_to_cm():
    assert abs(u.feet_to_cm(1.0) - 30.48) < 1e-6


def test_pounds_to_grams():
    assert abs(u.pounds_to_grams(1.0) - 453.59237) < 1e-6


def test_parse_measurement():
    v, unit = u.parse_measurement("6 ft")
    assert v == 6
    assert unit == "ft"
