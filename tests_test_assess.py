from Desafio_Bonus.models import PrimordialDuck, DroneInfo, Location
from Desafio_Bonus.assess import assess_capture


def test_assess_capture_basic():
    drone = DroneInfo(serial="x", brand="b", manufacturer="m", country="BR")
    loc = Location(city="c", country="BR", latitude=0.0, longitude=0.0)
    duck = PrimordialDuck(id="t", drone=drone, height_cm=150, weight_g=20000, location=loc, gps_precision_m=5, status="transe", heart_bpm=80, mutations=5)
    ass = assess_capture(duck)
    assert ass.cost_estimate > 0
    assert 0 <= ass.risk_score <= 100
