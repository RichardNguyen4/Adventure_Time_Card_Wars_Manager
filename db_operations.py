import sqlite3
import csv

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

def get_collection_card_count():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""SELECT cards.card_name, SUM(collection.quantity_owned * sets_cards.card_count) AS total_count
                   FROM collection
                   JOIN sets_cards on collection.set_id = sets_cards.set_id
                   JOIN cards on sets_cards.card_id = cards.card_id
                   GROUP BY cards.card_name;
                   """)
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
    cursor.execute("""SELECT card_name
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
    cursor.execute("""SELECT sets.set_id, sets.set_name FROM sets_cards 
                   JOIN sets ON sets_cards.set_id = sets.set_id WHERE card_id = ?""", (card_id,))
    conn.commit()
    sets = cursor.fetchall()
    return sets

def write_collection_to_csv():
    collection_data = get_collection_card_count()

    with open("collection_data.csv", mode = "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Card Name","Count"])
        writer.writerows(collection_data)

if __name__ == "__main__":

    update_set_count_in_collections(1,0)
    update_set_count_in_collections(2,0)
    print(get_all_collection())

    write_collection_to_csv()

    