import sqlite3
import pandas as pd


database = "adventuretimecardwars.db"
conn = sqlite3.connect(r"adventuretimecardwars.db")
cursor = conn.cursor()
cursor.execute 

def write_cards():
    df = pd.read_csv("cards.csv", usecols=["name", "image_name"])

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
    set_list = ["Collector's Pack #1: Finn vs Jake", 
                "Collector's Pack #2: BMO vs Lady Rainicorn", 
                "Collector's Pack #3: Princess Bubblegum vs Lumpy Space Princess",
                "Collector's Pack #4: Ice King vs Marceline",
                "Collector's Pack #5: Lemongrab vs Gunter",
                "Collector's Pack #6: Fiona vs Cake",
                "Doubles Tournament",
                "Ultimate Collection",
                "For The Glory Booster Collection",
                "10th Anniversary Kickstarter"]

    for set in set_list:
    
        cursor.execute("""
                    INSERT INTO sets (set_name)
                    VALUES (:set)""", 
                    ((set,))
                    )
        print (f"{set} was added!")
    
    conn.commit()

def write_cards_to_set(deck_csv, set_number):

    if decks_exist(deck_csv):
        decklist = pd.read_csv(deck_csv, usecols=["Card Name", "Quantity"])
    
        for _, row in decklist.iterrows():
            card_name = row["Card Name"]
            card_quantity = row["Quantity"]
            cursor.execute("""
                            SELECT card_id
                            FROM cards
                            WHERE card_name = ?""", 
                            (card_name,)
                            )
            card_id = cursor.fetchone()
            card_id = card_id[0]

                           
            cursor.execute("""
                           INSERT INTO sets_cards (card_id, set_id, card_count)
                           VALUES (:card_id, :set_id, :quantity)""", 
                           ((card_id), (set_number), (card_quantity))
                           )

        conn.commit()

def decks_exist(deck_csv):
    decklist = pd.read_csv(deck_csv, usecols=["Card Name", "Quantity"])

    for _, row in decklist.iterrows():
        card_name = row['Card Name']
        if not cards_exist(card_name):
            print(f'{card_name} cannot be found in the database')
            return False
        
    return True
        

def cards_exist(card_name):
    cursor.execute("""SELECT COUNT(*)
                    FROM cards 
                    WHERE card_name = ?""", (card_name,))
    return cursor.fetchone()[0]
                

if __name__ == "__main__":

    write_cards_to_set("FinnList.csv", 1)
    
    conn.close()







