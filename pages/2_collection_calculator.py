import streamlit as st
import db_operations as db
import pandas as pd


st.title("Collection Calculator")
st.write("Input the number of each set you own!")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Your Collection")
    pack1 = st.selectbox("Collector's Pack #1: Finn vs Jake", [0, 1, 2, 3, 4, 5], (db.get_set_count_from_collections(1)))
    pack2 = st.selectbox("Collector's Pack #2: BMO vs Lady Rainicorn", [0, 1, 2, 3, 4, 5], db.get_set_count_from_collections(2))
    pack3 = st.selectbox("Collector's Pack #3: Princess Bubblegum vs LSP", [0, 1, 2, 3, 4, 5], db.get_set_count_from_collections(3))
    pack4 = st.selectbox("Collector's Pack #4: Ice King vs Marceline", [0, 1, 2, 3, 4, 5], db.get_set_count_from_collections(4))
    pack5 = st.selectbox("Collector's Pack #5: Lemongrab vs Gunter", [0, 1, 2, 3, 4, 5], db.get_set_count_from_collections(5))

with col2:
    st.subheader("")
    pack6 = st.selectbox("Collector's Pack #6: Fiona vs Cake", [0, 1, 2, 3, 4, 5], db.get_set_count_from_collections(6))
    doubles_tournament = st.selectbox("Doubles Tournament", [0, 1, 2, 3, 4, 5], db.get_set_count_from_collections(7))
    ultimate_collection = st.selectbox("Ultimate Collection", [0, 1, 2, 3, 4, 5], db.get_set_count_from_collections(8))
    glory_booster = st.selectbox("For The Glory Booster Collection", [0, 1, 2, 3, 4, 5], db.get_set_count_from_collections(9))
    kickstarter = st.selectbox("10th Anniversary Kickstarter", [0, 1], db.get_set_count_from_collections(10))

col3, col4 = st.columns([2,7])

is_clicked_all_done = col3.button("Update Collection")

if is_clicked_all_done:
    
    sets = [
    (1, pack1),
    (2, pack2),
    (3, pack3),
    (4, pack4),
    (5, pack5),
    (6, pack6),
    (7, doubles_tournament),
    (8, ultimate_collection),
    (9, glory_booster),
    (10, kickstarter)
]
    for set_id, set_amount in sets:
        db.update_set_count_in_collections(set_id, set_amount)

    collection_data = db.get_collection_card_data()

    db.write_collection_to_csv(collection_data)

    col4.write("Collection has been Updated! Check your Collectin Search!")
