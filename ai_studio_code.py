import streamlit as st

# Configuración de la página
st.set_page_config(page_title="EndoNutri Tool", layout="wide")

# Estilos CSS para mejorar la apariencia
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #007bff; color: white; }
    .stExpander { background-color: white; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Título Principal
st.title("🩺 EndoNutri Suite")
st.sidebar.title("Navegación")
perfil = st.sidebar.radio("Seleccione Especialidad:", ["Endocrinología", "Nutrición"])

# ------------------------------------------------------------------
# MÓDULO ENDOCRINOLOGÍA
# ------------------------------------------------------------------
if perfil == "Endocrinología":
    st.header("Módulo de Endocrinología")
    sub_endo = st.selectbox("Subespecialidad:", ["Diabetes", "Hipófisis y Suprarrenales", "Metabolismo Fosfocálcico"])

    if sub_endo == "Diabetes":
        st.subheader("Calculadora de Insulina")
        col1, col2 = st.columns(2)
        with col1:
            glucemia = st.number_input("Glucemia actual (mg/dL)", value=150)
            objetivo = st.number_input("Glucemia objetivo (mg/dL)", value=100)
            sensibilidad = st.number_input("Factor Sensibilidad (ISF)", value=50)
        with col2:
            raciones = st.number_input("Raciones de CH (1 ración=10g)", value=4.0)
            ratio = st.number_input("Ratio Insulina/Ración", value=1.0)
        
        if st.button("Calcular Dosis"):
            dosis_correccion = (glucemia - objetivo) / sensibilidad
            dosis_prandial = raciones * ratio
            total = max(0, dosis_correccion + dosis_prandial)
            st.success(f"Dosis Total Sugerida: {round(total, 1)} unidades")
            st.info(f"Corrección: {round(dosis_correccion, 1)} U | Prandial: {round(dosis_prandial, 1)} U")

    elif sub_endo == "Hipófisis y Suprarrenales":
        tab1, tab2 = st.tabs(["Test de Nugent (Cushing)", "Test de ACTH (ISR)"])
        with tab1:
            st.write("**Protocolo:** Administrar 1mg dexametasona a las 23:00h. Medir cortisol a las 08:00h.")
            cortisol = st.number_input("Resultado Cortisol (µg/dL)", key="nugent")
            if cortisol > 0:
                if cortisol < 1.8: st.success("Supresión normal (< 1.8 µg/dL)")
                else: st.error("Falta de supresión. Sugiere Hipercortisolismo.")
        with tab2:
            st.write("**Protocolo:** Medir cortisol basal, administrar 250µg ACTH IV. Medir a los 30 y 60 min.")
            c60 = st.number_input("Cortisol 60 min (µg/dL)", key="acth")
            if c60 > 0:
                if c60 >= 18: st.success("Respuesta normal (≥ 18 µg/dL)")
                else: st.error("Sugerente de Insuficiencia Suprarrenal.")

    elif sub_endo == "Metabolismo Fosfocálcico":
        st.subheader("Manejo de Calcemia")
        c1, c2, c3 = st.columns(3)
        ca_med = c1.number_input("Calcio medido (mg/dL)", value=8.5)
        alb = c2.number_input("Albúmina (g/dL)", value=4.0)
        fosf = c3.number_input("Fósforo (mg/dL)", value=3.5)
        
        ca_corr = ca_med + 0.8 * (4.0 - alb)
        st.metric("Calcio Corregido", f"{round(ca_corr, 2)} mg/dL")

        if ca_corr > 10.5:
            st.warning("**Sugerencia Hipercalcemia:** Hidratación con SSF 0.9%. Considerar Bifosfonatos si >12 o síntomas.")
        elif ca_corr < 8.5:
            st.warning("**Sugerencia Hipocalcemia:**")
            if fosf > 4.5: st.info("P elevado: Evaluar función renal o Hipoparatiroidismo.")
            else: st.info("P bajo/normal: Evaluar déficit de Vitamina D o Magnesio.")
            st.write("- Tratamiento: Gluconato Cálcico 10% IV (agudo) o Calcio oral + Calcitriol.")

# ------------------------------------------------------------------
# MÓDULO NUTRICIÓN
# ------------------------------------------------------------------
else:
    st.header("Módulo de Nutrición")
    tab_n1, tab_n2 = st.tabs(["Harris-Benedict", "Nutrición Parenteral"])

    with tab_n1:
        sexo = st.radio("Sexo", ["Hombre", "Mujer"])
        peso = st.number_input("Peso (kg)", value=70.0)
        talla = st.number_input("Talla (cm)", value=170.0)
        edad = st.number_input("Edad (años)", value=50)
        factor = st.selectbox("Factor de Estrés/Actividad", [1.0, 1.2, 1.3, 1.5])

        if sexo == "Hombre":
            geb = 66.47 + (13.75 * peso) + (5 * talla) - (6.75 * edad)
        else:
            geb = 655.1 + (9.56 * peso) + (1.85 * talla) - (4.67 * edad)
        
        st.success(f"Gasto Energético Total: {round(geb * factor, 0)} kcal/día")

    with tab_n2:
        st.subheader("Cálculo de Aportes NPT")
        col_a, col_b = st.columns(2)
        with col_a:
            proteina_g = st.number_input("Proteína deseada (g/kg)", value=1.2)
            na_sangre = st.number_input("Sodio analítica (mEq/L)", value=135)
        with col_b:
            k_sangre = st.number_input("Potasio analítica (mEq/L)", value=3.5)
            vol_total = st.number_input("Volumen total NPT (ml)", value=2000)

        st.markdown("---")
        st.write("**Sugerencia de Modificaciones:**")
        # Lógica de Iones
        if na_sangre < 135: st.info("⬆️ Aumentar Na en NPT (Déficit detectado)")
        if k_sangre < 3.5: st.info("⬆️ Aumentar K en NPT (Aporte sugerido 1-2 mEq/kg)")
        
        st.write(f"- Aporte proteico total: {round(proteina_g * peso, 1)} g/día")
        st.write(f"- Ritmo de infusión: {round(vol_total/24, 1)} ml/h")