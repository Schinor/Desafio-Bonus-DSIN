import json
import tempfile
from pathlib import Path
import importlib.util
import importlib
import sys

import streamlit as st
import folium
from streamlit_folium import st_folium


def load_module_from_path(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


BASE_DIR = Path(__file__).parent


def load_ducks_from_path(path: Path):
    # Import modules directly from the current directory
    models_mod = load_module_from_path(BASE_DIR / "models.py", "models")
    utils_mod = load_module_from_path(BASE_DIR / "utils.py", "utils")

    raw = json.loads(path.read_text())
    ducks = []
    for item in raw:
        d = item["drone"]
        drone = models_mod.DroneInfo(serial=d["serial"], brand=d.get("brand", ""), manufacturer=d.get("manufacturer", ""), country=d.get("country", ""))

        h_val, h_unit = utils_mod.parse_measurement(item["height"])
        height_cm = utils_mod.to_cm(h_val, h_unit)

        w_val, w_unit = utils_mod.parse_measurement(item["weight"])
        weight_g = utils_mod.to_grams(w_val, w_unit)

        loc = item.get("location", {})
        ref = utils_mod.lookup_reference(loc.get("latitude", 0.0), loc.get("longitude", 0.0))
        location = models_mod.Location(city=loc.get("city", ""), country=loc.get("country", ""), latitude=loc.get("latitude", 0.0), longitude=loc.get("longitude", 0.0), reference_point=ref)

        p_val, p_unit = utils_mod.parse_measurement(item.get("gps_precision", "0 m"))
        gps_precision_m = utils_mod.precision_to_meters(p_val, p_unit)

        sp = None
        if item.get("superpower"):
            spj = item["superpower"]
            sp = models_mod.SuperPower(name=spj["name"], description=spj["description"], classification=spj["classification"])

        duck = models_mod.PrimordialDuck(
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


def main():
    st.set_page_config(page_title="Desafio-Bonus — Primordial Ducks", layout="wide")

    st.title("Primordial Ducks — Catalog & Drone Control")

    st.sidebar.header("Dataset")
    data_choice = st.sidebar.radio("Fonte de dados:", ["sample_data.json", "Upload JSON"])

    ducks = []
    data_path = BASE_DIR / "sample_data.json"

    if data_choice == "sample_data.json":
        try:
            ducks = load_ducks_from_path(data_path)
        except Exception as e:
            st.error(f"Erro ao carregar dados de exemplo: {e}")
            st.stop()
    else:
        uploaded = st.sidebar.file_uploader("Envie um arquivo JSON com o formato do desafio", type=["json"])
        if uploaded is not None:
            try:
                # write to temp file then reuse existing loader
                with tempfile.NamedTemporaryFile("w", delete=False, suffix=".json", encoding="utf-8") as tf:
                    tf.write(uploaded.read().decode("utf-8"))
                    temp_path = Path(tf.name)
                ducks = load_ducks_from_path(temp_path)
            except Exception as e:
                st.error(f"Erro ao processar upload: {e}")
                st.stop()
        else:
            st.info("Envie um arquivo JSON ou selecione o dataset de exemplo.")

    if not ducks:
        st.warning("Nenhum pato carregado.")
        return

    # list ducks in sidebar
    st.sidebar.header("Patos catalogados")
    duck_ids = [d.id for d in ducks]
    sel = st.sidebar.selectbox("Selecione um pato:", duck_ids)
    duck = next((d for d in ducks if d.id == sel), None)

    if duck is None:
        st.warning("Pato selecionado não encontrado.")
        return

    # show details
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader(f"Detalhes — {duck.id}")
        st.write("**Drone**")
        st.write(f"Serial: {duck.drone.serial}")
        st.write(f"Marca: {duck.drone.brand} — País: {duck.drone.country}")

        st.write("---")
        st.write("**Medidas**")
        st.write(f"Altura: {duck.height_cm:.1f} cm")
        st.write(f"Peso: {duck.weight_g:.1f} g")
        st.write(f"Status: {duck.status}")
        if duck.heart_bpm:
            st.write(f"Batimentos: {duck.heart_bpm} bpm")
        st.write(f"Mutations: {duck.mutations}")
        if duck.superpower:
            st.write("**Superpoder**")
            st.write(f"Nome: {duck.superpower.name}")
            st.write(f"Classificação: {duck.superpower.classification}")
            st.write(f"Descrição: {duck.superpower.description}")

        st.write("---")
        st.write("**Localização**")
        st.write(f"{duck.location.city}, {duck.location.country}")
        st.write(f"Lat/Lon: {duck.location.latitude}, {duck.location.longitude}")
        if duck.location.reference_point:
            st.write(f"Ponto de referência: {duck.location.reference_point}")

    with col2:
        st.subheader("Ações")
        # Import modules directly from the current directory
        assess_mod = load_module_from_path(BASE_DIR / "assess.py", "assess")
        drone_mod = load_module_from_path(BASE_DIR / "drone.py", "drone")

        if st.button("Avaliar captura"):
            try:
                assessment = assess_mod.assess_capture(duck)
                st.metric("Custo estimado", f"${assessment.cost_estimate}")
                st.metric("Risco", f"{assessment.risk_score}%")
                st.write(f"Poder militar: {assessment.military_power}")
                st.write(f"Valor científico: {assessment.scientific_value}")
                st.write("Recomendado:")
                for t in assessment.recommended_tooling:
                    st.write(f"- {t}")
                if assessment.rationale:
                    st.info(assessment.rationale)
            except Exception as e:
                st.error(f"Erro na avaliação: {e}")

        st.write("---")
        st.write("**Simular drone**")
        if st.button("Planejar ataque"):
            try:
                dc = drone_mod.DroneController(id=f"control-{duck.id}")
                plan = dc.plan_attack(duck)
                st.write(plan)
            except Exception as e:
                st.error(f"Erro ao planejar: {e}")

        if st.button("Engajar (simular)"):
            try:
                dc = drone_mod.DroneController(id=f"control-{duck.id}")
                outcome = dc.engage(duck)
                st.write("Resultado:")
                st.json(outcome)
            except Exception as e:
                st.error(f"Erro na simulação: {e}")

    # Interactive map and drone controls
    st.write("---")
    st.subheader("Mapa e controle de voo")
    import pandas as pd
    # Sidebar controls for base and drone
    st.sidebar.markdown("---")
    st.sidebar.header("🏠 Base DSIN")
    if 'base_lat' not in st.session_state:
        st.session_state.base_lat = 0.0
    if 'base_lon' not in st.session_state:
        st.session_state.base_lon = 0.0
    
    base_lat = st.sidebar.number_input(
        "Latitude da base", 
        value=st.session_state.base_lat, 
        format="%f",
        key="base_lat_input"
    )
    base_lon = st.sidebar.number_input(
        "Longitude da base", 
        value=st.session_state.base_lon, 
        format="%f",
        key="base_lon_input"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.header("✈️ Controles do Drone")

    # session DroneController initialization
    if "controller" not in st.session_state:
        st.session_state.controller = None

    # ensure drone module is available for controller creation
    try:
        drone_mod
    except NameError:
        drone_mod = load_module_from_path(BASE_DIR / "drone.py", "drone")

    if st.sidebar.button("Criar/Resetar controlador"):
        controller = drone_mod.DroneController(id="control-st")
        # Inicializa o drone na posição da base usando os valores da session_state
        controller.lat = st.session_state.base_lat
        controller.lon = st.session_state.base_lon
        st.session_state.controller = controller
        st.sidebar.success("Controlador criado na base")

    # prepare dataframe for st.map including ducks, base and drone (if any)
    rows = []
    for d in ducks:
        rows.append({"lat": d.location.latitude, "lon": d.location.longitude, "label": d.id, "type": "duck"})

    # include base
    rows.append({"lat": base_lat, "lon": base_lon, "label": "base", "type": "base"})

    # include drone if present in session
    drone_marker = None
    if "controller" in st.session_state and st.session_state.controller is not None:
        ctrl = st.session_state.controller
        # Inicializa as coordenadas do drone se não existirem
        if not hasattr(ctrl, 'lat'):
            ctrl.lat = st.session_state.base_lat
        if not hasattr(ctrl, 'lon'):
            ctrl.lon = st.session_state.base_lon
        
        # Permite ajuste manual da posição do drone via controles
        ctrl.lat = st.sidebar.number_input(
            "Latitude do drone",
            value=float(ctrl.lat),
            format="%f",
            key="drone_lat_input"
        )
        ctrl.lon = st.sidebar.number_input(
            "Longitude do drone",
            value=float(ctrl.lon),
            format="%f",
            key="drone_lon_input"
        )
        
        rows.append({"lat": ctrl.lat, "lon": ctrl.lon, "label": ctrl.id, "type": "drone"})
        drone_marker = (ctrl.lat, ctrl.lon)

    df = pd.DataFrame(rows)

    # Create a folium map centered on the first duck's position
    center_lat = df[df['type'] == 'duck']['lat'].iloc[0]
    center_lon = df[df['type'] == 'duck']['lon'].iloc[0]
    m = folium.Map(location=[center_lat, center_lon], zoom_start=4)

    # Add markers with different colors for each type
    for _, row in df.iterrows():
        if row['type'] == 'duck':
            color = 'red'
            icon = 'info-sign'
        elif row['type'] == 'base':
            color = 'blue'
            icon = 'home'
        else:  # drone
            color = 'green'
            icon = 'plane'

        folium.Marker(
            [row['lat'], row['lon']],
            popup=row['label'],
            icon=folium.Icon(color=color, icon=icon)
        ).add_to(m)
    
    # Display the map
    st_folium(m, width=800)

    # show legend info
    st.write("Legenda:")
    st.write("- 🔴 Vermelho: pato primitivo")
    st.write("- 🔵 Azul: base DSIN") 
    st.write("- 🟢 Verde: posição atual do drone (se criado/voado)")

    # show controller status and flight action (uses base_lat/base_lon defined above)
    if st.session_state.controller is None:
        st.info("Crie um controlador para testar voos e verificações de status.")
    else:
        ctrl = st.session_state.controller
        st.write("**Drone status**")
        s = ctrl.status()
        st.write(s)

        st.write("**Voar até o pato selecionado**")
        if st.button("Fly to pato selecionado"):
            try:
                # use approximate distance calculation (this is a simplification)
                from math import sqrt, pow
                lat_diff = abs(base_lat - duck.location.latitude)
                lon_diff = abs(base_lon - duck.location.longitude)
                utils_pkg = load_module_from_path(BASE_DIR / "utils.py", "utils")
                dist_km = sqrt(pow(lat_diff, 2) + pow(lon_diff, 2)) * 111  # rough conversion to km
                ctrl.fly_to(duck.location.latitude, duck.location.longitude, dist_km)
                # Atualiza a posição do drone após o voo
                ctrl.lat = duck.location.latitude
                ctrl.lon = duck.location.longitude
                st.success(f"Voo simulado: {dist_km:.2f} km. Battery now: {ctrl.battery:.2f}")
                st.write({"battery": ctrl.battery, "fuel": ctrl.fuel, "integrity": ctrl.integrity})
                st.write("Histórico:")
                for h in ctrl.history:
                    st.write(f"- {h}")
            except Exception as e:
                st.error(f"Erro ao simular voo: {e}")


if __name__ == "__main__":
    main()
