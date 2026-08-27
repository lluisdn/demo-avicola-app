import streamlit as st
import pandas as pd
from datetime import datetime, date

# Configuració de la pàgina
st.set_page_config(page_title="Avícola Serlluis — Encàrrecs", page_icon="🍗", layout="wide")

# Llista de botigues de Terrassa
BOTIGUES = [
    "C/ Galileu, 113",
    "Av. Béjar, 226",
    "Av. Josep Tarradellas, 13",
    "Av. Àngel Sallent, 115",
    "Av. Jacquard, 38"
]

# Inicialització corregida (format d'items homogeni)
if "orders" not in st.session_state:
    st.session_state.orders = [
        {
            "id": "ORD-101",
            "client": "Jordi Mas",
            "telefon": "612345678",
            "botiga": "C/ Galileu, 113",
            "data_recollida": str(date.today()),
            "hora_recollida": "11:30",
            "items": [
                {"nom": "Entrecot de Vedella", "cant": 1.0, "unitat": "kg"},
                {"nom": "Mandonguilles amb salsa", "cant": 1.0, "unitat": "kg"}
            ],
            "observacions": " ",
            "total": 28.00,
            "estat": "En preparació",
            "pagat": True
        }
    ]

# Capçalera de l'aplicació
st.title("🍗 Avícola Serlluis")
st.caption("Sistema Digital d'Encàrrecs Online i Control de Producció per a l'Obrador")

modo_vista = st.radio("🔄 Canvia de vista per a la demo:", ["📱 Vista Client", "👨‍🍳 Vista Botiga"], horizontal=True)

st.divider()

if modo_vista == "📱 Vista Client":
    st.header("🛒 Fes el teu encàrrec i estalvia't les cues")
    st.write("Tria els teus productes, selecciona la botiga i l'hora de recollida, i tindrem la comanda a punt.")

    st.subheader("1. Selecciona els teus productes")

    catalog = {
        "🥩 Carns Fresques i Talls": [
            {
                "id": "entrecot_vedella",
                "nom": "Entrecot de Vedella",
                "preu": 15.50,
                "unitat": "kg",
                "step": 0.1,
                "desc": "Vedella de criança pròpia, tallat tendre i suculent ideal per fer a la planxa o a la brasa.",
                "img": "https://www.avicolaserlluis.com/images/entrecot.jpg" 
            },
            {
                "id": "llaminera_porc",
                "nom": "Llaminera de Porc",
                "preu": 11.20,
                "unitat": "kg",
                "step": 0.1,
                "desc": "Tallat prim per fer a la planxa, molt baix en greix i proteïna d'alta qualitat.",
                "img": "https://www.avicolaserlluis.com/images/llaminera.jpg"
            },
            {
                "id": "cuixetes_pollastre",
                "nom": "Cuixetes de Pollastre",
                "preu": 10.80,
                "unitat": "kg",
                "step": 0.1,
                "desc": "Trossos de pollastre fresc ideals per a paelles, rostits al forn o guisats casolans.",
                "img": "https://www.avicolaserlluis.com/images/cuixes%20pollastre.jpg"
            }
        ],
        "🧆 Plats Cuinats": [
            {
                "id": "ensaladilla",
                "nom": "Ensaladilla Casolana",
                "preu": 5.00,
                "unitat": "ud",
                "step": 1.0,
                "desc": "Elaboració tradicional diària amb patata, tonyina, verduretes i maionesa cremosa.",
                "img": "https://www.avicolaserlluis.com/images/ensaladilla.jpg"
            },
            {
                "id": "rulo_espinacs",
                "nom": "Espinacs amb rul.lo de cabra",
                "preu": 4.50,
                "unitat": "ud",
                "step": 1.0,
                "desc": "Plat elaborat a l'obrador amb espinacs frescos, pinyons i un suau toc de formatge de cabra.",
                "img": "https://www.avicolaserlluis.com/images/espinacs%20amb%20rulo%20cabra.jpg"
            },
            {
                "id": "fricando_vedella",
                "nom": "Fricandó de vedella amb salsa",
                "preu": 14.80,
                "unitat": "kg",
                "step": 0.1,
                "desc": "Tallat prim de vedella guisat lentament amb xampinyons i moixernons en la seva salsa tradicional.",
                "img": "https://www.avicolaserlluis.com/images/fricando%20de%20vedella%20amb%20salsa.jpg"
            },
            {
                "id": "mandonguilles",
                "nom": "Mandonguilles amb salsa",
                "preu": 12.50,
                "unitat": "kg",
                "step": 0.1,
                "desc": "Mandonguilles mixtes casolanes rostides lentament amb sofregit d'all i ceba.",
                "img": "https://www.avicolaserlluis.com/images/mandonguilles%20amb%20salsa.jpg"
            }
        ],
        "🥓 Xarcuteria": [
            {
                "id": "llonganissa_iberica",
                "nom": "Llonganissa Ibèrica",
                "preu": 18.50,
                "unitat": "kg",
                "step": 0.1,
                "desc": "Embotit de curació artesanal amb aromes intenses, ideal per a entrepans o fustes d'embotits.",
                "img": "https://www.avicolaserlluis.com/images/llonganissa%20iberica.jpg"
            },
            {
                "id": "catalana_trufada",
                "nom": "Catalana trufada",
                "preu": 13.20,
                "unitat": "kg",
                "step": 0.1,
                "desc": "Recepta tradicional de l'obrador amb un toc subtil de trufa negra.",
                "img": "https://www.avicolaserlluis.com/images/catalana%20trufada.jpg"
            }
        ]
    }

    selected_items = []

    for category_name, products in catalog.items():
        with st.expander(category_name, expanded=False):
            for prod in products:
                with st.container(border=True):
                    col_img, col_info = st.columns([1, 2])
                    
                    with col_img:
                        try:
                            st.image(prod["img"], use_container_width=True)
                        except Exception:
                            st.image("https://placehold.co/150x150/e0e0e0/333333?text=Sense+Imatge", use_container_width=True)
                    
                    with col_info:
                        st.markdown(f"**{prod['nom']}**")
                        st.caption(prod["desc"])
                        st.markdown(f"**{prod['preu']:.2f} €** / {prod['unitat']}")
                        
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
                        
                        if cant > 0:
                            selected_items.append({
                                "nom": prod["nom"],
                                "cant": cant,
                                "unitat": prod["unitat"],
                                "preu": prod["preu"],
                                "subtotal": cant * prod["preu"]
                            })

    total_comanda = sum(item["subtotal"] for item in selected_items)

    st.markdown(f"### 💰 **Total Encàrrec:** `{total_comanda:.2f} €`")

    if total_comanda > 0:
        st.divider()
        st.subheader("2. Dades de recollida i punt de lliurament")
        
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            nom_client = st.text_input("Nom i Cognoms")
            tel_client = st.text_input("Telèfon de contacte (per avisos SMS/WhatsApp)")
            botiga_rec = st.selectbox("Botiga de recollida", BOTIGUES)
        
        with col_c2:
            data_rec = st.date_input("Data de recollida", min_value=date.today())
            hora_rec = st.selectbox("Hora aproximada de recollida", ["09:30", "10:30", "11:30", "12:30", "13:30", "17:30", "18:30", "19:30"])
            obs_client = st.text_area("Indicacions especials pel tallador/obrador", placeholder="Ex: El pollastre a octaus, tallat ben prim...")

        st.subheader("3. Confirmació i Pagament")
        st.info("💡 **Integració de pagament pròxima:** Aquest pas s'enllaçarà directament amb Stripe / Redsys per a pagament amb targeta o Bizum.")
        
        if st.button("💳 Pagar i Confirmar Encàrrec", type="primary", use_container_width=True):
            if nom_client and tel_client:
                nova_comanda = {
                    "id": f"ORD-{len(st.session_state.orders) + 101}",
                    "client": nom_client,
                    "telefon": tel_client,
                    "botiga": botiga_rec,
                    "data_recollida": str(data_rec),
                    "hora_recollida": hora_rec,
                    "items": selected_items,
                    "observacions": obs_client,
                    "total": total_comanda,
                    "estat": "Pendent",
                    "pagat": True
                }
                
                st.session_state.orders.append(nova_comanda)
                st.success(f"✅ Encàrrec registrat correctament! Codi comanda: **{nova_comanda['id']}** (Botiga: {botiga_rec}). Rebràs un avís quan estigui a punt.")
            else:
                st.warning("⚠️ Per favor, omple el teu nom i telèfon per poder identificar l'encàrrec.")

# ==========================================
# VISTA 2: BOTIGA / OBRADOR (PANEL INTERN)
# ==========================================
else:
    st.header("👨‍🍳 Panel de Gestió de Comandes")
    st.write("Visibilitat en temps real dels encàrrecs rebuts.")

    if not st.session_state.orders:
        st.info("No hi ha comandes registrades de moment.")
    else:
        botiga_filtre = st.selectbox("🔍 Filtrar comandes per botiga:", ["Totes"] + BOTIGUES)
        comandes_filtrades = st.session_state.orders if botiga_filtre == "Totes" else [o for o in st.session_state.orders if o.get('botiga') == botiga_filtre]

        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric("Total Comandes", len(comandes_filtrades))
        with col_m2:
            pendents = sum(1 for o in comandes_filtrades if o['estat'] in ['Pendent', 'En preparació'])
            st.metric("Encàrrecs per Preparar", pendents)
        with col_m3:
            total_recaudat = sum(o['total'] for o in comandes_filtrades if o['pagat'])
            st.metric("Facturació Digital", f"{total_recaudat:.2f} €")

        st.divider()

        st.subheader("📋 Resum Consolidat de Producció (Totals a Tallar i Plegar)")
        
        totals_produccio = {}
        for order in comandes_filtrades:
            # Si la comanda ve en el format nou (llista de diccionaris)
            if isinstance(order['items'], list):
                for item in order['items']:
                    clau = f"{item['nom']} ({item['unitat']})"
                    totals_produccio[clau] = totals_produccio.get(clau, 0.0) + item['cant']
            # Control de seguretat per si hi ha comandes en el format antic (diccionari simple)
            elif isinstance(order['items'], dict):
                for nom, val in order['items'].items():
                    totals_produccio[nom] = totals_produccio.get(nom, "")

        if totals_produccio:
            df_prod = pd.DataFrame([
                {"Producte": k, "Quantitat Total Necessària": f"{v:.1f}" if isinstance(v, float) and "kg" in k else f"{v}"} 
                for k, v in totals_produccio.items()
            ])
            st.dataframe(df_prod, use_container_width=True, hide_index=True)
        else:
            st.write("Cap producte pendent de producció.")

        st.divider()

        st.subheader("📦 Comandes Rebutes")
        
        for idx, order in enumerate(comandes_filtrades):
            botiga_info = order.get('botiga', 'Botiga no especificada')
            with st.expander(f"🔴 Comanda {order['id']} — {order['client']} ({order['hora_recollida']}h) — {botiga_info} — Estat: {order['estat']}"):
                c1, c2 = st.columns(2)
                with c1:
                    st.write(f"**Client:** {order['client']}")
                    st.write(f"**Telèfon:** {order['telefon']}")
                    st.write(f"**Botiga Recollida:** {botiga_info}")
                    st.write(f"**Data Recollida:** {order['data_recollida']} a les {order['hora_recollida']}h")
                    st.write(f"**Observacions de tall:** {order['observacions'] if order['observacions'] else 'Cap'}")
                
                with c2:
                    st.write("**Detall de l'encàrrec:**")
                    if isinstance(order['items'], list):
                        for item in order['items']:
                            st.write(f"- {item['nom']}: **{item['cant']} {item['unitat']}**")
                    elif isinstance(order['items'], dict):
                        for k, v in order['items'].items():
                            st.write(f"- {k}: **{v}**")
                            
                    st.write(f"**Total Pagat:** `{order['total']:.2f} €` ✅")

                real_idx = st.session_state.orders.index(order)
                nou_estat = st.selectbox(
                    "Actualitzar estat de la comanda:",
                    ["Pendent", "En preparació", "A punt per recollir", "Lliurada"],
                    index=["Pendent", "En preparació", "A punt per recollir", "Lliurada"].index(order['estat']),
                    key=f"estat_{order['id']}"
                )
                st.session_state.orders[real_idx]['estat'] = nou_estat

# ==========================================
# PEU DE PÀGINA / BANDA HORITZONTAL DE CONTACTE
# ==========================================
st.markdown("<br><br>", unsafe_allow_html=True)

footer_html = """
<div style="
    background-color: #1E293B;
    color: #F8FAFC;
    padding: 24px 32px;
    border-radius: 12px;
    margin-top: 40px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
">
    <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 16px;">
        <div>
            <h4 style="margin: 0 0 6px 0; color: #F1F5F9; font-size: 1.1rem;">🛠️ Desenvolupament i Suport Tècnic</h4>
            <p style="margin: 0; color: #94A3B8; font-size: 0.9rem;">Desenvolupat per a la gestió digital d'Avícola Serlluis</p>
        </div>
        <div style="display: flex; flex-wrap: wrap; gap: 24px; align-items: center; font-size: 0.95rem;">
            <div>👤 <strong>Desenvolupador:</strong> Lluís Deixt Nadal</div>
            <div>🔗 <strong>LinkedIn:</strong> <a href="https://www.linkedin.com/in/lluisdeixt/" target="_blank" style="color: #38BDF8; text-decoration: none;">linkedin.com/in/elteuperfil</a></div>
            <div>✉️ <strong>Email:</strong> lluisdn2000@gmail.com</div>
            <div>📞 <strong>Telèfon:</strong> 668 83 11 67</div>
        </div>
    </div>
</div>
"""

st.markdown(footer_html, unsafe_allow_html=True)
