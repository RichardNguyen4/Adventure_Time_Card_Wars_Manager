import streamlit as st
import pandas as pd
import db_operations as db
import os
from st_aggrid import AgGrid, GridOptionsBuilder


st.title("CardWars Collection Search")

# Load CSV data
data_frame = pd.read_csv("collection_data.csv")

# **Search Bar**
search_query = st.text_input("Search for a card", "").strip().lower()

col1, col2 = st.columns(2)
# **Filter DataFrame based on search input**
if search_query:
    filtered_df = data_frame[data_frame["Card Name"].str.lower().str.contains(search_query, na=False)]
else:
    filtered_df = data_frame  # Show all data if no search is entered

with col1:
    # **Ag-Grid Configuration**
    gb = GridOptionsBuilder.from_dataframe(filtered_df)
    gb.configure_selection(selection_mode="single")  # Allow row selection
    gb.configure_column("Card Name", headerCheckboxSelection=True)  # Allow selecting rows

    grid_options = gb.build()

    # **Display Ag-Grid**
    grid_response = AgGrid(
    filtered_df,
    gridOptions=grid_options,
    height=470,
    fit_columns_on_grid_load=True,
    theme="streamlit",  # Other options: "light", "streamlit", "alpine" 
    )

with col2:
    try:
        selected_name = grid_response.selected_data["Card Name"]

        card_image = db.get_image_from_card_name(selected_name.iloc[0])

        card_image_path = os.path.join("images", card_image)

        st.image(card_image_path)

    except TypeError:
        path = r"images/back_HD.jpg"
        st.image(path)