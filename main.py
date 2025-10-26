import json
from pathlib import Path

from .models import DroneInfo, Location, PrimordialDuck, SuperPower
from .utils import parse_measurement, to_cm, to_grams, precision_to_meters, lookup_reference
from .assess import assess_capture
from .drone import DroneController


DATA_FILE = Path(__file__).parent / "sample_data.json"


def load_and_catalog(path: Path):
	raw = json.loads(path.read_text())
	ducks = []
	for item in raw:
		# parse drone
		d = item["drone"]
		drone = DroneInfo(serial=d["serial"], brand=d.get("brand", ""), manufacturer=d.get("manufacturer", ""), country=d.get("country", ""))

		# parse height
		h_val, h_unit = parse_measurement(item["height"])
		height_cm = to_cm(h_val, h_unit)

		w_val, w_unit = parse_measurement(item["weight"])
		weight_g = to_grams(w_val, w_unit)

		loc = item.get("location", {})
		ref = lookup_reference(loc.get("latitude", 0.0), loc.get("longitude", 0.0))
		location = Location(city=loc.get("city", ""), country=loc.get("country", ""), latitude=loc.get("latitude", 0.0), longitude=loc.get("longitude", 0.0), reference_point=ref)

		p_val, p_unit = parse_measurement(item.get("gps_precision", "0 m"))
		gps_precision_m = precision_to_meters(p_val, p_unit)

		sp = None
		if item.get("superpower"):
			spj = item["superpower"]
			sp = SuperPower(name=spj["name"], description=spj["description"], classification=spj["classification"])

		duck = PrimordialDuck(
			id=item["id"],
			drone=drone,
			height_cm=height_cm,
			weight_g=weight_g,
			location=location,
			gps_precision_m=gps_precision_m,
			status=item.get("status", "hibernacao profunda"),
			heart_bpm=item.get("heart_bpm"),
			mutations=item.get("mutations", 0),
			superpower=sp,
		)
		ducks.append(duck)
	return ducks


def main_demo():
	ducks = load_and_catalog(DATA_FILE)

	print(f"Cataloged {len(ducks)} Primordial Ducks:\n")
	for d in ducks:
		print(f"ID: {d.id}")
		print(f"  Drone: {d.drone.serial} ({d.drone.brand}) from {d.drone.country}")
		print(f"  Height: {d.height_cm:.1f} cm, Weight: {d.weight_g:.1f} g")
		print(f"  Location: {d.location.city}, {d.location.country} ({d.location.latitude},{d.location.longitude})")
		if d.location.reference_point:
			print(f"   Reference: {d.location.reference_point}")
		print(f"  GPS precision: {d.gps_precision_m:.2f} m")
		print(f"  Status: {d.status}")
		if d.heart_bpm:
			print(f"  Heart BPM: {d.heart_bpm}")
		print(f"  Mutations: {d.mutations}")
		if d.superpower:
			print(f"  Superpower: {d.superpower.name} - {d.superpower.classification}")

		assessment = assess_capture(d)
		print(f"  -> Assessment: cost={assessment.cost_estimate}, risk={assessment.risk_score}, military={assessment.military_power}, scientific_value={assessment.scientific_value}")

		# simulate a drone engagement for demonstration
		drone = DroneController(id=f"control-{d.id}")
		outcome = drone.engage(d)
		print(f"  Drone outcome: success={outcome['success']}, remaining={outcome['remaining_status']}\n")


if __name__ == "__main__":
	main_demo()

