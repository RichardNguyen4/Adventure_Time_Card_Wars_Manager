# Card Wars Collection Manager

![Card Wars Logo](images/back_HD.jpg)  

## 📌 Overview
**Card Wars Collection Manager** is a **Python and SQLite-based** application built with **Streamlit** to help users **track, organize, and manage** their **Adventure Time: Card Wars** collection.  

## 🚀 Features
- **Collection Calculator**: Input the number of sets you own and update your collection.
- **Collection Search**: Search for any card in your collection.
- **Missing Collection Tracker**: Identify missing cards and find which sets contain them.
- **Database Integration**: Uses **SQLite** to store and manage card data.
- **Interactive UI**: Built with **Streamlit** and **Ag-Grid** for smooth browsing.


## 🏆 Purpose  
This project is for **collectors** and **trading card enthusiasts** who want a **centralized** and **automated way** to manage their **Adventure Time: Card Wars** collection.

## 📥 Installation  

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/yourusername/CardWars-Collection-Manager.git
   cd CardWars-Collection-Manager

2. **Install Dependencies**
    pip install -r requirements.txt

3. **Run the Application**
    streamlit run Home.py

## ⚙️ How to Use
Start with the Collection Calculator

Input the sets you own.
Click "Update Collection" to save changes.
Search for Cards

Use the Collection Search feature to browse your collection.
Find Missing Cards

Set a minimum threshold of copies for each card.
Get a list of missing cards and which sets contain them.

## 🛠️ Built With
Python
Streamlit
SQLite
Pandas
st-aggrid (for interactive tables)