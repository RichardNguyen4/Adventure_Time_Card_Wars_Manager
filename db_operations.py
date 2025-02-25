import sqlite3

def connect_db():
    return sqlite3.connect("adventuretimecardwars.db")

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



