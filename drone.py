import random
from typing import List, Optional
from models import PrimordialDuck, CaptureAssessment, SuperPower


class DroneController:
    def __init__(self, id: str, battery_pct: float = 100.0, fuel_l: float = 10.0, integrity_pct: float = 100.0):
        self.id = id
        self.battery = float(battery_pct)
        self.fuel = float(fuel_l)
        self.integrity = float(integrity_pct)
        self.history: List[str] = []

    def fly_to(self, lat: float, lon: float, distance_km: float):
        # simple consumption model
        battery_cost = min(50, distance_km * 0.5)
        fuel_cost = min(self.fuel, distance_km * 0.1)
        self.battery = max(0.0, self.battery - battery_cost)
        self.fuel = max(0.0, self.fuel - fuel_cost)
        self.history.append(f"Flew {distance_km} km to {lat},{lon}")
        return True

    def status(self):
        return {"battery": self.battery, "fuel": self.fuel, "integrity": self.integrity}

    def identify_weakness(self, duck: PrimordialDuck) -> List[str]:
        weaknesses = []
        # heuristic weaknesses
        if duck.weight_g > 50000:
            weaknesses.append("slow_mobility")
        if duck.height_cm > 200:
            weaknesses.append("top_attack_vulnerable")
        if duck.superpower:
            sp = duck.superpower.classification.lower()
            if "bélico" in sp or "belico" in sp or "alto" in sp:
                weaknesses.append("requires_heavy_armor")
            if "raro" in sp:
                weaknesses.append("unknown_countermeasures")
        # random chance
        if random.random() < 0.2:
            weaknesses.append(random.choice(["chocolate_attraction", "sonic_disruption", "slippery_slope"]))
        return weaknesses

    def plan_attack(self, duck: PrimordialDuck) -> str:
        weaknesses = self.identify_weakness(duck)
        plan = []
        if "top_attack_vulnerable" in weaknesses:
            plan.append("Drop heavy payload from altitude > 50m")
        if "slow_mobility" in weaknesses:
            plan.append("Encircle and restrain using nets")
        if "requires_heavy_armor" in weaknesses:
            plan.append("Deploy armored support units")
        if "chocolate_attraction" in weaknesses:
            plan.append("Use chocolate as bait (deploy cake-laden volunteers)")
        if not plan:
            plan.append("Standard capture routine: stun darts then net")
        # resource check
        if duck.height_cm > 100:
            plan.append("Preferred approach: aerial strike + containment")
        self.history.append(f"Planned attack for {duck.id}: {plan}")
        return "; ".join(plan)

    def random_defense(self, weakness_tag: Optional[str] = None) -> str:
        # emulates the bizarre defenses described in prompt
        defenses = [
            "teleport_children_with_sweets",
            "deploy_confetti_shield",
            "activate_electric_mirror",
            "release_hella_smoke_bombs",
        ]
        if weakness_tag == "chocolate_attraction":
            return "teleport_children_with_sweets"
        return random.choice(defenses)

    def engage(self, duck: PrimordialDuck) -> dict:
        plan = self.plan_attack(duck)
        chosen_defense = self.random_defense(None)
        # simulate outcome
        success = random.random() > 0.3
        outcome = {
            "planned_actions": plan,
            "defense_used": chosen_defense,
            "success": success,
            "remaining_status": self.status(),
        }
        if not success:
            self.integrity -= random.uniform(5, 40)
        return outcome
