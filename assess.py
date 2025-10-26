from models import PrimordialDuck, CaptureAssessment


def assess_capture(duck: PrimordialDuck, base_lat: float = 0.0, base_lon: float = 0.0) -> CaptureAssessment:
    # simplistic distance-based cost: not implementing full haversine for brevity
    # cost factors: size, weight, distance-est (approx), status, mutations
    size_factor = max(1.0, duck.height_cm / 50.0)
    weight_factor = max(1.0, duck.weight_g / 10000.0)
    status_factor = 1.0
    risk = 0.0
    military = "light"
    rationale_parts = []

    if duck.status == "desperto":
        status_factor = 2.5
        risk += 30
        military = "heavy"
        rationale_parts.append("Desperto: alto risco")
    elif duck.status == "transe":
        status_factor = 1.5
        risk += 10
        military = "medium"
        rationale_parts.append("Transe: risco moderado (pode despertar)")
        if duck.heart_bpm and duck.heart_bpm > 120:
            risk += 15
            rationale_parts.append("Batimentos altos: chance de despertar")
    else:
        # hibernação profunda
        status_factor = 0.8
        risk += 2
        military = "light"
        rationale_parts.append("Hibernação profunda: risco reduzido")

    mutation_value = min(100, duck.mutations * 5)
    scientific_value = mutation_value * 1.2

    cost = 1000.0 * size_factor * weight_factor * status_factor
    # gps precision affects risk/cost
    if duck.gps_precision_m > 10:
        cost *= 1.2
        risk += 5
        rationale_parts.append("Baixa precisão GPS: maior custo de busca")

    # superpower adjustments
    if duck.superpower:
        cls = duck.superpower.classification.lower()
        if "bélico" in cls or "belico" in cls:
            risk += 25
            military = "very heavy"
            rationale_parts.append("Superpoder bélico: alto risco")
        if "raro" in cls:
            scientific_value += 30
            rationale_parts.append("Superpoder raro: alto valor científico")

    # normalize risk
    risk = min(100.0, risk + duck.mutations * 1.5)

    recommended = ["net", "stun_darts"]
    if military in ("heavy", "very heavy"):
        recommended.append("armored_support")

    rationale = "; ".join(rationale_parts)

    return CaptureAssessment(
        id=duck.id,
        cost_estimate=round(cost, 2),
        military_power=military,
        risk_score=round(risk, 2),
        scientific_value=round(scientific_value, 2),
        recommended_tooling=recommended,
        rationale=rationale,
    )
