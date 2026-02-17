import streamlit as st
import pandas as pd
import numpy as np

# --- CONFIGURACIÓN Y ESTILOS ---
st.set_page_config(page_title="EndoPro Advanced", layout="wide")
st.markdown("""
    <style>
    .reportview-container { background: #f0f2f6; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); }
    .section-box { border: 1px solid #d1d8e0; padding: 20px; border-radius: 10px; margin-bottom: 20px; background: white; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: NAVEGACIÓN PRINCIPAL ---
st.sidebar.title("🩺 EndoNutri v2.0")
perfil = st.sidebar.radio("Seleccione Perfil:", ["Endocrinología", "Nutrición"])

# ------------------------------------------------------------------
# MÓDULO ENDOCRINOLOGÍA
# ------------------------------------------------------------------
if perfil == "Endocrinología":
    menu_endo = st.sidebar.selectbox("Área:", ["Diabetes", "Hipófisis", "Suprarrenales", "Tiroides", "Metabolismo Fosfocálcico"])

    # --- DIABETES ---
    if menu_endo == "Diabetes":
        st.header("Gestión Avanzada de Diabetes")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Factor de Sensibilidad (FS)")
            t_insulina = st.number_input("Dosis Total Diaria (TDD)", value=40.0)
            regla = st.selectbox("Regla aplicada", [1800, 1500], help="1800 para análogos rápidos, 1500 para cristalina")
            fs = regla / t_insulina
            st.metric("FS calculado", f"{round(fs, 1)} mg/dL por 1 UI")
        
        with col2:
            st.subheader("Análisis de Glucemias")
            archivo_pdf = st.file_uploader("Subir PDF Curvas (14 días)", type=["pdf"])
            if not archivo_pdf:
                g_desayuno = st.number_input("Glucemia Desayuno (media)", value=140)
                g_comida = st.number_input("Glucemia Comida (media)", value=130)
                g_cena = st.number_input("Glucemia Cena (media)", value=160)
        
        st.subheader("Tratamiento Actual y Ajustes")
        c1, c2, c3, c4 = st.columns(4)
        lenta = c1.number_input("Insulina Lenta", value=20)
        r_des = c2.number_input("Rápida Desayuno", value=6)
        r_com = c3.number_input("Rápida Comida", value=8)
        r_cen = c4.number_input("Rápida Cena", value=6)

        if st.button("Analizar y Sugerir Modificación"):
            # Lógica simplificada de ajuste
            sugerencia = ""
            if g_desayuno > 130: sugerencia += f"- Aumentar Lenta en +2 UI (Glucemia basal alta: {g_desayuno})\n"
            if g_comida > 180: sugerencia += f"- Aumentar Rápida Desayuno en +1 o 2 UI\n"
            if g_cena > 180: sugerencia += f"- Aumentar Rápida Comida en +1 o 2 UI\n"
            
            if sugerencia == "": st.success("Control óptimo. No se sugieren cambios.")
            else: st.warning(sugerencia)

    # --- HIPÓFISIS ---
    elif menu_endo == "Hipófisis":
        st.header("Unidad de Hipófisis")
        
        tipo_test = st.selectbox("Herramienta:", ["IGF-1 SDS", "Déficit de Agua y Sodio", "Osmolaridad"])
        
        if tipo_test == "IGF-1 SDS":
            metodo = st.selectbox("Método:", ["iSYS (IDS)", "Liaison (DiaSorin)", "Immulite (Siemens)"])
            valor_igf1 = st.number_input("IGF-1 Medido (ng/mL)", value=200.0)
            edad = st.number_input("Edad del paciente", value=30)
            # Nota: Aquí irían las tablas de referencia según método/edad
            st.info("Cálculo basado en medias normativas para el método seleccionado...")
            st.metric(f"SDS {metodo}", "En desarrollo (Requiere tablas específicas)")

        elif tipo_test == "Déficit de Agua y Sodio":
            peso = st.number_input("Peso (kg)", value=70.0)
            na_act = st.number_input("Sodio Actual (mEq/L)", value=125.0)
            na_obj = st.number_input("Sodio Objetivo", value=135.0)
            
            # Déficit de Sodio
            def_na = 0.6 * peso * (na_obj - na_act)
            st.metric("Déficit de Sodio", f"{round(def_na, 1)} mEq")
            
            # Tratamiento
            st.subheader("Sugerencia de Reposición")
            sf = (def_na / 154) * 1000  # Salino Fisiológico 0.9% tiene 154 mEq/L
            sh = (def_na / 513) * 1000  # Salino Hipertónico 3% tiene 513 mEq/L
            st.write(f"- Volumen de SF 0.9% necesario: {round(sf, 0)} ml")
            st.write(f"- Volumen de SH 3% necesario: {round(sh, 0)} ml")

        elif tipo_test == "Osmolaridad":
            na = st.number_input("Sodio", value=140.0)
            glu = st.number_input("Glucosa (mg/dL)", value=100.0)
            urea = st.number_input("BUN (mg/dL)", value=15.0)
            osm = (2 * na) + (glu / 18) + (urea / 2.8)
            st.metric("Osmolaridad Plasmática", f"{round(osm, 1)} mOsm/kg")

    # --- SUPRARRENALES ---
    elif menu_endo == "Suprarrenales":
        st.header("Unidad Suprarrenal")
        opc = st.radio("Herramienta:", ["Ferriman-Gallwey", "Equivalencia Corticoides", "Ratio Aldosterona/ARP"])
        
        if opc == "Ferriman-Gallwey":
            st.write("Suma de puntuación (0-4) en 9 áreas:")
            areas = ["Labio superior", "Mentón", "Pecho", "Espalda superior", "Espalda inferior", "Abdomen superior", "Abdomen inferior", "Brazos", "Muslos"]
            total = 0
            for a in areas:
                total += st.slider(a, 0, 4, 0)
            st.metric("Puntuación Total", total)
            if total >= 8: st.error("Hirsutismo clínico")

        elif opc == "Equivalencia Corticoides":
            dosis = st.number_input("Dosis (mg)", value=5.0)
            tipo = st.selectbox("Corticoide:", ["Hidrocortisona", "Prednisona", "Metilprednisolona", "Dexametasona"])
            equiv = {"Hidrocortisona": 20, "Prednisona": 5, "Metilprednisolona": 4, "Dexametasona": 0.75}
            ref = dosis / equiv[tipo]
            st.write("**Equivalencias:**")
            for k, v in equiv.items():
                st.write(f"{k}: {round(v * ref, 2)} mg")

    # --- TIROIDES ---
    elif menu_endo == "Tiroides":
        st.header("Análisis TI-RADS")
        img = st.file_uploader("Subir Imagen Ecográfica", type=["jpg", "png", "jpeg"])
        if img:
            st.image(img, caption="Ecografía subida", width=300)
            st.info("Simulando análisis de imagen... (Requiere integración con IA de Visión)")
            
        st.subheader("Clasificación Manual Dirigida")
        p1 = st.selectbox("Composición:", ["Quístico (0)", "Espongiforme (0)", "Mixto (1)", "Sólido (2)"])
        p2 = st.selectbox("Ecocgenicidad:", ["Anecoico (0)", "Hiperecogénico/Iso (1)", "Hipoecoico (2)", "Muy Hipoecoico (3)"])
        p3 = st.selectbox("Forma:", ["Más ancho que alto (0)", "Más alto que ancho (3)"])
        p4 = st.selectbox("Margen:", ["Liso (0)", "Mal definido (0)", "Lobulado/Irregular (2)", "Extensión extratiroidea (3)"])
        p5 = st.selectbox("Focos ecogénicos:", ["Ninguno (0)", "Macrocalcificaciones (1)", "Calcificaciones periféricas (2)", "Focos punctantes (3)"])
        
        # Lógica de puntos (extrayendo el número entre paréntesis)
        puntos = sum([int(x.split('(')[1][0]) for x in [p1, p2, p3, p4, p5]])
        
        if puntos <= 1: tr = "TI-RADS 1 (Benigno)"
        elif puntos == 2: tr = "TI-RADS 2 (No sospechoso)"
        elif puntos == 3: tr = "TI-RADS 3 (Leve sospecha)"
        elif puntos >= 7: tr = "TI-RADS 5 (Alta sospecha)"
        else: tr = "TI-RADS 4 (Moderada sospecha)"
        
        st.metric("Resultado", tr)

    # --- FOSFOCÁLCICO ---
    elif menu_endo == "Metabolismo Fosfocálcico":
        st.header("Metabolismo Mineral")
        st.subheader("Manejo de Hipocalcemia Crónica")
        
        c1, c2 = st.columns(2)
        with c1:
            ca_act = st.number_input("Calcio Actual (mg/dL)", value=7.5)
            p_act = st.number_input("Fósforo Actual (mg/dL)", value=4.5)
        with c2:
            rocal_act = st.number_input("Rocaltrol actual (mcg/día)", value=0.25)
            ca_oral = st.number_input("Calcio oral actual (mg/día)", value=1000)
            
        if st.button("Sugerir Ajuste"):
            if ca_act < 8.0:
                st.warning(f"Calcio bajo ({ca_act}). Sugerencia: Aumentar Rocaltrol a {rocal_act + 0.25} mcg o Calcio a {ca_oral + 500} mg.")
            elif ca_act > 9.5:
                st.success(f"Calcio alto/límite. Sugerencia: Reducir Rocaltrol.")
            if p_act > 5.0:
                st.error("Fósforo elevado. Considerar quelantes o reducir dosis de Vitamina D activa.")

# ------------------------------------------------------------------
# MÓDULO NUTRICIÓN
# ------------------------------------------------------------------
else:
    st.header("Soporte Nutricional Avanzado")
    
    # 1. Harris-Benedict
    with st.expander("1. Cálculo de Requerimientos (Harris-Benedict)", expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        sexo = col1.radio("Sexo", ["H", "M"])
        peso = col2.number_input("Peso (kg)", value=70.0)
        talla = col3.number_input("Talla (cm)", value=170)
        edad = col4.number_input("Edad", value=50)
        
        if sexo == "H": geb = 66.47 + (13.75*peso) + (5*talla) - (6.75*edad)
        else: geb = 655.1 + (9.56*peso) + (1.85*talla) - (4.67*edad)
        
        st.metric("GEB", f"{int(geb)} kcal/día")

    # 2. Sugerencia de Bolsa NPT
    with st.expander("2. Diseño de Bolsa NPT", expanded=True):
        st.subheader("Composición Sugerida")
        # Ratios estándar
        prot_g = peso * 1.5
        nitro_g = prot_g / 6.25
        hc_g = (geb * 0.5) / 4
        lip_g = (geb * 0.3) / 9
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Proteínas (Nitrógeno)", f"{round(prot_g,1)}g ({round(nitro_g,1)}g N)")
        c2.metric("Hidratos de Carbono", f"{round(hc_g,1)} g")
        c3.metric("Lípidos", f"{round(lip_g,1)} g")
        
        st.markdown("**Electrólitos Estándar (mEq):**")
        st.write(f"Sodio: 60-100 | Potasio: 60 | Magnesio: 10-15 | Fósforo: 20-30 mmol | Calcio: 10")

    # 3. Ajuste por Analítica
    with st.expander("3. Ajuste de Iones por Analítica", expanded=True):
        st.info("Introduzca la analítica actual para modificar la bolsa")
        col_an1, col_an2, col_an3 = st.columns(3)
        k_lab = col_an1.number_input("Potasio Lab (mEq/L)", value=3.0)
        na_lab = col_an2.number_input("Sodio Lab (mEq/L)", value=132.0)
        mg_lab = col_an3.number_input("Magnesio Lab (mg/dL)", value=1.4)
        
        if st.button("Calcular Modificación de Bolsa"):
            if k_lab < 3.5:
                st.warning(f"K bajo ({k_lab}). Sugerencia: Aumentar Potasio en NPT de 60 mEq a 80 mEq.")
            if na_lab < 135:
                st.warning(f"Na bajo ({na_lab}). Sugerencia: Aumentar Sodio en NPT a 100-120 mEq.")
            if mg_lab < 1.7:
                st.warning(f"Mg bajo ({mg_lab}). Sugerencia: Añadir 5 mEq extras de Magnesio.")