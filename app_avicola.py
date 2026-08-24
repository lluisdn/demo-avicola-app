import streamlit as st
import pandas as pd
from datetime import datetime, date, time

# Configuració de la pàgina
st.set_page_config(page_title="Avícola Serlluis — Encàrrecs", page_icon="🍗", layout="wide")

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
st.title("🍗 Avícola Serlluis")
st.caption("Sistema Digital d'Encàrrecs Online i Control de Producció per a l'Obrador")

# Selector de Vista per a la Demo
modo_vista = st.radio("🔄 Canvia de vista per a la demo:", ["📱 Vista Client", "👨‍🍳 Vista Botiga "], horizontal=True)

st.divider()

# ==========================================
# VISTA 1: CLIENT (ENCÀRRECS ONLINE)
# ==========================================
if modo_vista == "📱 Vista Client (Encàrrecs Online)":
    st.header("🛒 Fes el teu encàrrec i estalvia't les cues")
    st.write("Tria els teus productes, selecciona l'hora de recollida i nosaltres tindrem la comanda a punt.")

# Catàleg de productes estructurat per categories i optimitzat per a mòbil
    st.subheader("1. Selecciona els teus productes")

    # Estructura de dades del catàleg
    # NOTA: Per utilitzar imatges reals, canvia la URL 'https://via.placeholder.com/...' 
    # per la ruta local de la imatge (ex: "assets/pollastre.jpg") o un enllaç direct d'internet.
    catalog = {
        "🥩 Carns Fresques i Talls": [
            {
                "id": "pollastre_groc",
                "nom": "Pollastre Groc Català",
                "preu": 9.50,
                "unitat": "kg",
                "step": 0.5,
                "desc": "Pollastre de creixement lent, carn ferm i saborosa ideal per fer al forn o guisat.",
                "img": "https://via.placeholder.com/150/e6c894/333333?text=Pollastre"
            },
            {
                "id": "pit_indi",
                "nom": "Pit de Gall d'Indi Tallat",
                "preu": 11.20,
                "unitat": "kg",
                "step": 0.5,
                "desc": "Tallat prim per fer a la planxa, molt baix en greix i proteïna d'alta qualitat.",
                "img": "https://via.placeholder.com/150/f0d3b7/333333?text=Gall+d'Indi"
            },
            {
                "id": "conill_fresc",
                "nom": "Conill de Granja Tallat",
                "preu": 10.80,
                "unitat": "kg",
                "step": 0.5,
                "desc": "Trossos ideals per a paelles o guisats amb xocolata i fons d'all.",
                "img": "https://via.placeholder.com/150/d1b89d/333333?text=Conill"
            }
        ],
        "🧆 Elaborats i Menjar Preparat": [
            {
                "id": "rodo_farcit",
                "nom": "Rodó de Gall d'Indi Farcit Tradicional",
                "preu": 14.80,
                "unitat": "kg",
                "step": 0.5,
                "desc": "Farcit de prunes, pinyons i carn picada. A punt per enfornar.",
                "img": "https://via.placeholder.com/150/c88e68/ffffff?text=Rodo+Farcit"
            },
            {
                "id": "hamb_alberginia",
                "nom": "Hamburguesa d'Albergínia i Formatge",
                "preu": 1.50,
                "unitat": "ud",
                "step": 1.0,
                "desc": "Elaboració pròpia diària amb verdura fresca i formatge d'ovella.",
                "img": "https://via.placeholder.com/150/7a5265/ffffff?text=Hamburguesa"
            },
            {
                "id": "croquetes_rostit",
                "nom": "Croquetes Casolanes de Rostit",
                "preu": 0.80,
                "unitat": "ud",
                "step": 1.0,
                "desc": "Massa cremosa feta amb el nostre rostit tradicional de festa major.",
                "img": "https://via.placeholder.com/150/d19c5c/ffffff?text=Croquetes"
            },
            {
                "id": "pollastre_ast",
                "nom": "Pollastre a l'Ast amb Patates",
                "preu": 12.50,
                "unitat": "ud",
                "step": 1.0,
                "desc": "Rostit lentament amb herbes aromàtiques i ració de patates inclosa.",
                "img": "https://via.placeholder.com/150/b5651d/ffffff?text=Pollastre+Ast"
            }
        ],
        "🥓 Embotits i Formatges": [
            {
                "id": "pernil_canaria",
                "nom": "Pernil Cuit Extra a la Canària",
                "preu": 18.50,
                "unitat": "kg",
                "step": 0.1,
                "desc": "Tallat prim per a sandvitxos o aperitius, baix en sal.",
                "img": "https://via.placeholder.com/150/e08b8b/ffffff?text=Pernil+Cuit"
            },
            {
                "id": "botifarra_ou",
                "nom": "Botifarra d'Ou Artesana",
                "preu": 13.20,
                "unitat": "kg",
                "step": 0.2,
                "desc": "Recepta tradicional de l'obrador, ideal per a taules d'embotits.",
                "img": "https://via.placeholder.com/150/e6bf73/333333?text=Botifarra+Ou"
            }
        ]
    }

    # Diccionari per guardar les seleccions de quantitat de l'usuari
    selected_quantities = {}

    # Renderitzat de categories en desplegables (Accordion UX per a mòbils)
    for category_name, products in catalog.items():
        with st.expander(category_name, expanded=False):
            for prod in products:
                with st.container(border=True):
                    col_img, col_info = st.columns([1, 2])
                    
                    with col_img:
                        # Imatge optimitzada sense opció de zoom
                        st.image(prod["img"], use_column_width=True)
                    
                    with col_info:
                        st.markdown(f"**{prod['nom']}**")
                        st.caption(prod["desc"])
                        st.markdown(f"**{prod['preu']:.2f} €** / {prod['unitat']}")
                        
                        # Selector adaptat al tipus d'unitat (kg decimal o unitat entera)
                        if prod["unitat"] == "kg":
                            cant = st.number_input(
                                f"Quantitat ({prod['unitat']}):",
                                min_value=0.0,
                                max_value=20.0,
                                step=prod["step"],
                                format="%.1f",
                                key=prod["id"]
                            )
                        else:
                            cant = st.number_input(
                                f"Quantitat ({prod['unitat']}):",
                                min_value=0,
                                max_value=50,
                                step=int(prod["step"]),
                                key=prod["id"]
                            )
                        
                        selected_quantities[prod["nom"]] = {
                            "cant": cant,
                            "preu": prod["preu"],
                            "unitat": prod["unitat"]
                        }

    # Càlcul automàtic del total
    total_comanda = sum(
        item["cant"] * item["preu"] for item in selected_quantities.values()
    )

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
