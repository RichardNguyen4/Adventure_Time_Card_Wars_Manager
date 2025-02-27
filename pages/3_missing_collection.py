import streamlit as st
import db_operations as db
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder


st.title("Missing Cards?")
col1, col2 = st.columns([8,2])

search_query = col1.text_input("Missing Card Search")
minimum_value = col2.number_input("Minimum Card Count", min_value=0, value=3, step=1)

st.write(f"To have {minimum_value} copies of each card, you are missing the following cards")

col3, col4 = st.columns([5,5])

if db.find_missing_cards(minimum_value):
    df = pd.DataFrame([row[:2] for row in (db.find_missing_cards(minimum_value))], columns=["Card Name", "Current Count"])
    
    if search_query:
        filtered_df = df[df["Card Name"].str.lower().str.contains(search_query, na=False)]
        
    else:
        filtered_df = df

    filtered_df["Missing Count"] = df.apply(lambda row: max(0, minimum_value - row["Current Count"]), axis=1)

    with col3:
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
    
    with col4:
        try:
            selected_name = grid_response.selected_data["Card Name"]
            selected_name = selected_name.iloc[0]
            
            card_id = db.get_card_id(selected_name)
            sets_with_card = db.get_sets(card_id)
            df = pd.DataFrame([row[1:] for row in sets_with_card], columns=["Found In", "Amount"])
            st.write(f"**{selected_name}** is found in the following sets")
            st.dataframe(df, use_container_width=True, hide_index=True )
        except TypeError:
            pass
    

        missing_cards = db.find_missing_cards(minimum_value)
        required_sets = db.required_sets(missing_cards, minimum_value)
        df = pd.DataFrame([(value[0], value[1]) for value in required_sets.values()], columns=["Sets to Complete Collection", "Copies"])
        st.dataframe(df, use_container_width=True, hide_index=True )


else:
    st.write(f"Congrats! you have {minimum_value} of each card")












