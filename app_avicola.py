import streamlit as st
import pandas as pd
from datetime import datetime, date, time

# Configuració de la pàgina
st.set_page_config(page_title="Avícola Sant Lluís — Encàrrecs", page_icon="🍗", layout="wide")

# Inicialització del sistema de persistència de comandes a la sessió (Simulació de Base de Dades)
if "orders" not in st.session_state:
    st.session_state.orders = [
        {
            "id": "ORD-101",
            "client": "Jordi Mas",
            "telefon": "612345678",
            "data_recollida": str(date.today()),
            "hora_recollida": "11:30",
            "items": {"Polastre Groc Català (kg)": 1.5, "Hamburguesa de Fit-Gall d'Albergínia (unitats)": 4},
            "observacions": "El pollastre tallat a octaus, si us plau.",
            "total": 18.50,
            "estat": "En preparació",
            "pagat": True
        }
    ]

# Estils visual de la capçalera
st.title("🍗 Avícola Sant Lluís — Des de 1968")
st.caption("Sistema Digital d'Encàrrecs Online i Control de Producció per a l'Obrador")

# Selector de Vista per a la Demo
modo_vista = st.radio("🔄 Canvia de vista per a la demo:", ["📱 Vista Client (Encàrrecs Online)", "👨‍🍳 Vista Botiga / Obrador (Recepció de Comandes)"], horizontal=True)

st.divider()

# ==========================================
# VISTA 1: CLIENT (ENCÀRRECS ONLINE)
# ==========================================
if modo_vista == "📱 Vista Client (Encàrrecs Online)":
    st.header("🛒 Fes el teu encàrrec i estalvia't les cues")
    st.write("Tria els teus productes frescos o elaborats, selecciona l'hora de recollida i nosaltres tindrem la comanda a punt.")

    # Catàleg de productes
    st.subheader("1. Selecciona els teus productes")
    
    col_prod1, col_prod2 = st.columns(2)
    
    with col_prod1:
        st.markdown("### 🐔 Aves Fresques i Talls")
        cant_pollastre = st.number_input("Polastre Groc Català (€9.50/kg)", min_value=0.0, max_value=10.0, step=0.5, format="%.1f")
        cant_gall_dindi = st.number_input("Pit de Gall d'Indi Tallat (€11.20/kg)", min_value=0.0, max_value=10.0, step=0.5, format="%.1f")
        cant_farcit = st.number_input("Rodo de Gall d'Indi Farcit Tradicional (€14.80/kg)", min_value=0.0, max_value=10.0, step=0.5, format="%.1f")

    with col_prod2:
        st.markdown("### 🧆 Elaborats d'Obrador i Cuinats")
        cant_hamb = st.number_input("Hamburguesa Artensanal d'Albergínia i Formatge (€1.50/ud)", min_value=0, max_value=20, step=1)
        cant_croquetes = st.number_input("Croquetes Casolanes de Rostit (€0.80/ud)", min_value=0, max_value=30, step=2)
        cant_ast = st.number_input("Polastre a l'Ast Rostic amb Patates (€12.50/ud)", min_value=0, max_value=5, step=1)

    # Càlcul del total
    total_comanda = (cant_pollastre * 9.50) + (cant_gall_dindi * 11.20) + (cant_farcit * 14.80) + (cant_hamb * 1.50) + (cant_croquetes * 0.80) + (cant_ast * 12.50)

    st.markdown(f"### 💰 **Total Encàrrec:** `{total_comanda:.2f} €`")

    if total_comanda > 0:
        st.divider()
        st.subheader("2. Dades de recollida i preparació")
        
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            nom_client = st.text_input("Nom i Cognoms")
            tel_client = st.text_input("Telèfon de contacte (per avisos SMS/WhatsApp)")
        
        with col_c2:
            data_rec = st.date_input("Data de recollida", min_value=date.today())
            hora_rec = st.selectbox("Hora aproximada de recollida", ["09:30", "10:30", "11:30", "12:30", "13:30", "17:30", "18:30", "19:30"])

        obs_client = st.text_area("Indicacions especials pel tallador/obrador", placeholder="Ex: El pollastre a octaus, les croquetes separades en dues boses...")

        st.subheader("3. Confirmació i Pagament")
        st.info("💡 **Integració de pagament pròxima:** Aquest pas s'enllaça directament amb Stripe / Redsys per a pagament amb targeta o Bizum.")
        
        if st.button("💳 Pagar i Confirmar Encàrrec", type="primary", use_container_width=True):
            if nom_client and tel_client:
                # Creació del resum d'ítems seleccionats
                items_dict = {}
                if cant_pollastre > 0: items_dict["Polastre Groc Català (kg)"] = cant_pollastre
                if cant_gall_dindi > 0: items_dict["Pit de Gall d'Indi (kg)"] = cant_gall_dindi
                if cant_farcit > 0: items_dict["Rodó Farcit (kg)"] = cant_farcit
                if cant_hamb > 0: items_dict["Hamburgueses Albergínia (ud)"] = cant_hamb
                if cant_croquetes > 0: items_dict["Croquetes Rostit (ud)"] = cant_croquetes
                if cant_ast > 0: items_dict["Polastre l'Ast (ud)"] = cant_ast

                nova_comanda = {
                    "id": f"ORD-{len(st.session_state.orders) + 101}",
                    "client": nom_client,
                    "telefon": tel_client,
                    "data_recollida": str(data_rec),
                    "hora_recollida": hora_rec,
                    "items": items_dict,
                    "observacions": obs_client,
                    "total": total_comanda,
                    "estat": "Pendent",
                    "pagat": True
                }
                
                st.session_state.orders.append(nova_comanda)
                st.success(f"✅ Encàrrec registrat correctament! Codi comanda: **{nova_comanda['id']}**. Rebràs un avís quan estigui a punt.")
            else:
                st.warning("⚠️ Per favor, omple el teu nom i telèfon per poder identificar l'encàrrec.")

# ==========================================
# VISTA 2: BOTIGA / OBRADOR (PANEL INTERN)
# ==========================================
else:
    st.header("👨‍🍳 Panel de Gestió de Comandes — Obrador i Tauler")
    st.write("Visibilitat en temps real dels encàrrecs rebuts per organitzar la preparació i el tall de la matèria prima.")

    if not st.session_state.orders:
        st.info("No hi ha comandes registrades de moment.")
    else:
        # Mètriques d'estat
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric("Total Comandes Avui", len(st.session_state.orders))
        with col_m2:
            pendents = sum(1 for o in st.session_state.orders if o['estat'] in ['Pendent', 'En preparació'])
            st.metric("Encàrrecs per Preparar", pendents)
        with col_m3:
            total_recaudat = sum(o['total'] for o in st.session_state.orders if o['pagat'])
            st.metric("Facturació Digital", f"{total_recaudat:.2f} €")

        st.divider()

        # Resum d'ítems totals a preparar (Consolidat per a l'obrador)
        st.subheader("📋 Resum Consolidat de Producció (Quilovatge i Unitats a Plegar)")
        
        totals_produccio = {}
        for order in st.session_state.orders:
            for item, cant in order['items'].items():
                totals_produccio[item] = totals_produccio.get(item, 0) + cant

        df_prod = pd.DataFrame(list(totals_produccio.items()), columns=["Producte", "Quantitat Total Necessària"])
        st.dataframe(df_prod, use_container_width=True, hide_index=True)

        st.divider()

        # Detall de comandes individuals
        st.subheader("📦 Comandes Rebutes")
        
        for idx, order in enumerate(st.session_state.orders):
            with st.expander(f"🔴 Comanda {order['id']} — {order['client']} ({order['hora_recollida']}h) — Estat: {order['estat']}"):
                c1, c2 = st.columns(2)
                with c1:
                    st.write(f"**Client:** {order['client']}")
                    st.write(f"**Telèfon:** {order['telefon']}")
                    st.write(f"**Data Recollida:** {order['data_recollida']} a les {order['hora_recollida']}h")
                    st.write(f"**Observacions de tall:** {order['observacions'] if order['observacions'] else 'Cap'}")
                
                with c2:
                    st.write("**Detall de l'encàrrec:**")
                    for k, v in order['items'].items():
                        st.write(f"- {k}: **{v}**")
                    st.write(f"**Total Pagat:** `{order['total']:.2f} €` ✅")

                # Canvi d'estat dinàmic
                nou_estat = st.selectbox(
                    "Actualitzar estat de la comanda:",
                    ["Pendent", "En preparació", "A punt per recollir", "Lliurada"],
                    index=["Pendent", "En preparació", "A punt per recollir", "Lliurada"].index(order['estat']),
                    key=f"estat_{idx}"
                )
                st.session_state.orders[idx]['estat'] = nou_estat
