import streamlit as st

st.set_page_config(
    page_title="Card Wars Manager",
    page_icon=r"Evan_Tuchkov_Emoji/at_snail.png",
)


col1, col2, col3= st.columns([2,6,2]) 
col2.title("Welcome to the Card Wars Collection Manager!")
col1.image(r"Evan_Tuchkov_Emoji/at_finn.png")
col3.image(r"Evan_Tuchkov_Emoji/at_jake.png")

# Intro
st.markdown(
    "**Python and SQLite-based manager** for tracking, organizing, and counting your Card Wars collection."
)

# 📌 Sidebar Overview
with st.expander("📌 **Understanding the Sidebar**"):
    st.markdown("""
    - **Located on the left**  
    - Used to track, organize, and count your collection
    """)

# 📊 Collection Calculator
with st.expander("📊 **Collection Calculator (Start Here!)**"):
    st.markdown("""
    - Adjust sets in collection to match what you own  
    - Click **"Update Collection"** to refresh your data  
    - All your owned cards will appear in **Collection Search**
    """)

# Collection Search
with st.expander("🔍 **Collection Search**"):
    st.markdown("""
    - **After updating your collection**, search for your cards here  
    - Shows the cards you own and their count  
    - Click and search to view cards on the right
    """)

# Missing Collection
with st.expander("❌ **Missing Collection**"):
    st.markdown("""
    - Set a **minimum copies threshold** for each card  
    - Displays **missing cards and their sets**  
    - Shows **which sets you need** to complete your collection
    """)

# 🌍 External Link
st.markdown("🔗 **Want More?** Visit the [Dweeb Database!](https://carddweeb.com/CardDatabase)")


