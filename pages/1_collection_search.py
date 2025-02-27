import streamlit as st
import pandas as pd
import db_operations as db
import os
from st_aggrid import AgGrid, GridOptionsBuilder

# Set the title of the app
st.title("CardWars Collection Search")

# Load the Collection Data
data_frame = pd.read_csv("collection_data.csv")

# Search Bar
search_query = st.text_input("Search for a card", "").strip().lower()

# Filter DataFrame based on search input
if search_query:
    filtered_df = data_frame[data_frame["Card Name"].str.lower().str.contains(search_query, na=False)]
else:
    filtered_df = data_frame  # Show all data if no search term is entered

# Split Layout: Left (Table) - Right (Image)
col1, col2 = st.columns(2)

# Left Column: Card Search Table
with col1:
    # Ag-Grid Configuration
    gb = GridOptionsBuilder.from_dataframe(filtered_df)
    gb.configure_selection(selection_mode="single")  # Allow single row selection
    gb.configure_column("Card Name", headerCheckboxSelection=True)

    grid_options = gb.build()

    # Display Ag-Grid
    grid_response = AgGrid(
    filtered_df,
    gridOptions=grid_options,
    height=470, # Adjust Height
    fit_columns_on_grid_load=True,
    theme="streamlit",  # Other options: "light", "streamlit", "alpine" 
    )

# Right Column: Display Selected Card Image
with col2:
    # Check if a card is selected
    try:
        selected_name = grid_response.selected_data["Card Name"]

        # Retrieve the card image file name from the database
        card_image = db.get_image_from_card_name(selected_name.iloc[0])

        # Construct the image pat
        card_image_path = os.path.join("images", card_image)

        # Display the image
        st.image(card_image_path)

    # If there is not a card selected, display deflaut
    except TypeError:
        path = r"images/back_HD.jpg"
        st.image(path)