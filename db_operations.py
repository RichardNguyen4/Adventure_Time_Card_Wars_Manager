import sqlite3
import csv
from collections import defaultdict
import math
import os

def connect_db(database = "adventuretimecardwars.db"):
    return sqlite3.connect(database)

def get_all_cards():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cards")
    cards = cursor.fetchall()
    conn.close()
    return cards

def get_all_sets():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sets")
    sets = cursor.fetchall()
    conn.close()
    return sets

def get_all_collection():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM collection")
    collection = cursor.fetchall()
    conn.close()
    return collection

def get_collection_card_data(min_value = None):
    conn = connect_db()
    cursor = conn.cursor()
    query = ("""
            SELECT cards.card_name, SUM(collection.quantity_owned * sets_cards.card_count) AS total_count
            FROM collection
            JOIN sets_cards on collection.set_id = sets_cards.set_id
            JOIN cards on sets_cards.card_id = cards.card_id
            GROUP BY cards.card_name
            """)
    
    if min_value is not None:
        query = f"""
                SELECT card_name, total_count FROM (
                {query}
                ) WHERE total_count < ?;
                """
        cursor.execute(query, (min_value,))
    else:
        query += ';'
        cursor.execute(query)
    
    cards_in_collection = cursor.fetchall()
    conn.close()
    return cards_in_collection

def update_set_count_in_collections(set_id, count):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""UPDATE collection
                   SET quantity_owned = ?
                   WHERE set_id = ?""", (count, set_id))
    conn.commit()
    conn.close()

def check_card_exist(card_name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT card_id FROM cards WHERE card_name = ?", (card_name,))
    result = cursor.fetchone()
    conn.close
    if result:
        return result[0]
    else:
        return False

def add_card_to_cards(card_name):
    if not check_card_exist(card_name):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO cards (card_name) VALUES (?)", (card_name))
    else:
        print("Card already exist in the database")

def get_card_id(card_name):
    card_id = check_card_exist(card_name)
    return card_id if card_id else None

def get_card_name(card_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT card_name
                   FROM cards
                   WHERE card_id = ?""", (card_id,))
    
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return None

def delete_card_from_cards(card_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cards WHERE card_id = ?", (card_id,))
    conn.commit()
    conn.close()

def get_sets(card_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
                    SELECT sets.set_id, sets.set_name FROM sets_cards 
                    JOIN sets ON sets_cards.set_id = sets.set_id WHERE card_id = ?""", (card_id,))
    conn.commit()
    sets = cursor.fetchall()
    return sets

def write_collection_to_csv(collection_data):

    with open("collection_data.csv", mode = "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Card Name","Count"])
        writer.writerows(collection_data)

def required_sets(desired_copies=3):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
                SELECT cards.card_name, SUM(collection.quantity_owned * sets_cards.card_count) as total_count, cards.card_id
                FROM collection
                JOIN sets_cards ON collection.set_id = sets_cards.set_id
                JOIN cards ON sets_cards.card_id = cards.card_id
                GROUP BY cards.card_name, cards.card_id
                HAVING total_count < ?
                """, (desired_copies,))
    
    missing_cards = cursor.fetchall()

    if not missing_cards:
        conn.close()
        return []
    

    card_set_map = defaultdict(list) 

    for card_name, current_count, card_id in missing_cards:
        cursor.execute("""
                        SELECT sets.set_id, sets.set_name, sets_cards.card_count
                        FROM sets_cards
                        JOIN sets ON sets_cards.set_id = sets.set_id
                        WHERE sets_cards.card_id = ?""", (card_id,))
        
        sets_with_card = cursor.fetchall()
        
        for set_id, set_name, card_count in sets_with_card:
            if card_count > 0:
                copies_needed = max(0, desired_copies - current_count)
                sets_needed = math.ceil(copies_needed / card_count)
                if set_id not in card_set_map:
                    card_set_map[set_id] = (set_name, sets_needed)
                else:
                    # Keep the max number of sets needed
                    card_set_map[set_id] = (set_name, max(card_set_map[set_id][1], sets_needed))

    conn.close()
    # { set_id: [(set_name, sets_needed)] }

    if 8 in card_set_map:
        for set_id in {1, 2, 3, 4, 5, 6, 9}:
            card_set_map.pop(set_id, None)
        
    return card_set_map
    
def get_sets_from_card_id(card_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
                    SELECT sets.set_id, sets.set_name, sets_cards.card_count
                    FROM sets_cards
                    JOIN sets ON sets_cards.set_id = sets.set_id
                    WHERE sets_cards.card_id = ?""", (card_id,))
    
    sets_with_card = cursor.fetchall()
    conn.close()

    return sets_with_card

def get_image_from_card_name(card_name):
    conn = connect_db()
    cursor = conn.cursor()

    card_id = get_card_id(card_name)

    cursor.execute("""
                   SELECT card_image
                   FROM cards
                   WHERE card_id = ?
                   """, (card_id,))
    
    card_image = cursor.fetchone()

    return card_image[0]

    
