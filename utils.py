from typing import Tuple


def feet_to_cm(feet: float) -> float:
    return feet * 30.48


def pounds_to_grams(pounds: float) -> float:
    return pounds * 453.59237


def yards_to_meters(yards: float) -> float:
    return yards * 0.9144


def parse_measurement(value_with_unit: str) -> Tuple[float, str]:
    """Parse a measurement like '6.5 ft' or '200 cm' returning (value, unit).

    Accepts units: cm, m, ft, in, g, kg, lb, lbs, lbm, yards, yd, m, meters
    """
    s = value_with_unit.strip().lower()
    parts = s.split()
    if len(parts) == 1:
        # try to separate number and letters
        import re

        m = re.match(r"([0-9.+-eE]+)\s*([a-z%]+)", s)
        if m:
            return float(m.group(1)), m.group(2)
        raise ValueError(f"Cannot parse measurement: {value_with_unit}")
    else:
        val = float(parts[0].replace(',', '.'))
        unit = parts[1]
        return val, unit


def to_cm(value: float, unit: str) -> float:
    unit = unit.lower()
    if unit in ("cm", "centimeter", "centimetro", "centimetros"):
        return value
    if unit in ("m", "meter", "metros", "metros"):
        return value * 100.0
    if unit in ("ft", "feet", "foot", "pés", "pe", "pé"):
        return feet_to_cm(value)
    if unit in ("in", "inch", "polegada", "polegadas"):
        return value * 2.54
    # default assume cm
    return value


def to_grams(value: float, unit: str) -> float:
    unit = unit.lower()
    if unit in ("g", "gram", "grama", "gramas"):
        return value
    if unit in ("kg", "kilogram", "kilograma", "kilogramas"):
        return value * 1000.0
    if unit in ("lb", "lbs", "pound", "libra", "libras"):
        return pounds_to_grams(value)
    # default assume grams
    return value


def precision_to_meters(value: float, unit: str) -> float:
    unit = unit.lower()
    if unit in ("m", "meter", "metros"):
        return value
    if unit in ("cm", "centimetro", "centimetros"):
        return value / 100.0
    if unit in ("yd", "yard", "yards", "jarda", "jardas"):
        return yards_to_meters(value)
    if unit in ("mm",):
        return value / 1000.0
    # default assume meters
    return value


# small reference points mapping (stub)
REFERENCE_POINTS = {
    ( -22.947, -43.172): "Pico da Neblina",
}

def lookup_reference(lat: float, lon: float):
    # naive exact match - realistic system would do geospatial proximity search
    for (plat, plon), name in REFERENCE_POINTS.items():
        if abs(plat - lat) < 0.01 and abs(plon - lon) < 0.01:
            return name
    return None
