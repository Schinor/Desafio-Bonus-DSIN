Desafio-Bonus — Primordial Ducks Catalog and Drone Control

Este projeto implementa uma solução em Python para catalogar informações sobre "Patos Primordiais", avaliar custo/risco/valor de captura e simular um drone controlador que planeja e executa ações de captura.

Como usar

Executando o app Streamlit (Windows PowerShell)

```powershell
    streamlit run ./Desafio-Bonus/app.py
    streamlit tun app.py
```

# Desafio-Bonus — Primordial Ducks Catalog and Drone Control

Este projeto implementa uma solução em Python para catalogar informações sobre "Patos Primordiais", avaliar custo/risco/valor de captura e simular um drone controlador que planeja e executa ações de captura.

## Principais tecnologias e bibliotecas

- Python (código-fonte)
- Streamlit — interface web interativa (`app.py`)
- Folium — mapas interativos (marcadores, ícones)
- streamlit-folium — integração Folium + Streamlit
- pandas — preparação de tabelas/frames usados para plotagem
- pytest — testes automatizados (ex.: `test_assess.py`, `test_utils.py`)
- JSON — formato dos dados de entrada (`sample_data.json`)

## Arquivos e módulos-chave

- `app.py` — frontend Streamlit (mapa, controles, integração com demais módulos)
- `models.py` — modelos de domínio (PrimordialDuck, Location, SuperPower, etc.)
- `utils.py` — utilitários e conversões de unidades
- `drone.py` — `DroneController` e lógica de simulação de voo/ataque
- `assess.py` — heurística de avaliação de captura
- `sample_data.json` — exemplo de dados usados no app

## Executando o app Streamlit (Windows PowerShell)

```powershell
python -m pip install -r requirements.txt
streamlit run ./Desafio-Bonus/app.py
```

## Observações e dicas

- O projeto usa `st.session_state` para manter estado do controlador e da base entre interações.
- O mapa é renderizado com Folium e integrado ao Streamlit via `streamlit-folium`.
- Distâncias no app usam atualmente uma aproximação (graus -> km). Se preferir precisão geodésica, podemos adicionar a função Haversine em `utils.py`.

## Executando testes (pytest)

```powershell
python -m pip install -r requirements.txt
pytest -q
```

## Exemplo rápido de uso

1. Abra o app Streamlit com o comando acima.
2. No sidebar: defina a posição da base (🏠 Base DSIN) e crie o controlador (✈️ Controles do Drone).
3. Selecione um pato e utilize os botões para avaliar, planejar ou simular engajamento. Use "Fly to pato selecionado" para mover o drone no mapa.

---
