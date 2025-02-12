import sqlite3
import pandas as pd

csv_file = "cards.csv"
database = "adventuretimecardwars.db"

df = pd.read_csv(csv_file, usecols=["name", "image_name"])
conn = sqlite3.connect(r"adventuretimecardwars.db")
cursor = conn.cursor()
cursor.execute 

def write_cards(): 
    for _, row in df.iterrows():
        card_name = row['name']
        card_image = row['image_name']

        cursor.execute("""
                        INSERT INTO cards (card_name, card_image)
                        VALUES (:name, :image_name)
                        """, ((card_name), (card_image))
                        )

    conn.commit()

def write_sets():
    set_list = ["Collector’s Pack #1: Finn vs Jake", 
                "Collector’s Pack #2: BMO vs Lady Rainicorn", 
                "Collector’s Pack #3: Princess Bubblegum vs Lumpy Space Princess",
                "Collector’s Pack #4: Ice King vs Marceline",
                "Collector’s Pack #5: Lemongrab vs Gunter",
                "Collector’s Pack #6: Fiona vs Cake",
                "Doubles Tournament",
                "Ultimate Collection",
                "For The Glory Booster Collection",
                "10th Anniversary Kickstarter"]

    for set in set_list:
    
        cursor.execute("""
                    INSERT INTO sets (set_name)
                    VALUES (:set)
                    """, ((set,))
                    )
        print (f"{set} was added!")
    
    conn.commit()

    
if __name__ == "__main__":

    write_sets()
    
    conn.close()







