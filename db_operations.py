import sqlite3
import csv
from collections import defaultdict
import math


def connect_db(database = "adventuretimecardwars.db"):
    """
    Establish a connection to the SQLite database.
    :param database: Name of the database file.
    :return: SQLite connection object.
    """
    return sqlite3.connect(database)

def get_all_cards():
    """
    Retrieve all cards from the database.
    :return: List of tuples containing card data.
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cards")
    cards = cursor.fetchall()
    conn.close()
    return cards

def get_all_sets():
    """
    Retrieve all sets from the database.
    :return: List of tuples containing set data.
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sets")
    sets = cursor.fetchall()
    conn.close()
    return sets

def get_all_collection():
    """
    Retrieve all collection data from the database.
    :return: List of tuples containing collection data.
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM collection")
    collection = cursor.fetchall()
    conn.close()
    return collection

def get_collection_card_data(min_value = None):
    """
    Retrieve all cards in the collection and their total count.
    :param min_value: Optional filter for cards with total count below this value.
    :return: List of tuples containing card name and total count.
    """
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
    """
    Update the quantity of a set in the collection.
    :param set_id: ID of the set.
    :param count: New quantity value.
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""UPDATE collection
                   SET quantity_owned = ?
                   WHERE set_id = ?""", (count, set_id))
    conn.commit()
    conn.close()

def check_card_exist(card_name):
    """
    Check if a card exists in the database.
    :param card_name: Name of the card.
    :return: Card ID if found, False otherwise.
    """
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
    """
    Add a new card to the database if it does not exist.
    :param card_name: Name of the card.
    """
    if not check_card_exist(card_name):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO cards (card_name) VALUES (?)", (card_name))
    else:
        print("Card already exist in the database")

def get_card_id(card_name):
    """
    Retrieve the ID of a card given its name.
    :param card_name: Name of the card.
    :return: Card ID if found, None otherwise.
    """
    card_id = check_card_exist(card_name)
    return card_id if card_id else None

def get_card_name(card_id):
    """
    Retrieve the name of a card given its id.
    :param card_name: ID of the card.
    :return: Card Name if found, None otherwise.
    """
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
    """
    Remove a card from the database.
    :param card_id: ID of the card.
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cards WHERE card_id = ?", (card_id,))
    conn.commit()
    conn.close()

def get_sets(card_id):
    """
    Retrieve the List of Sets that a card is in given its ID.
    :param card_name: ID of the card.
    :return: SETS if found, None otherwise.
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
                    SELECT sets.set_id, sets.set_name, sets_cards.card_count FROM sets_cards 
                    JOIN sets ON sets_cards.set_id = sets.set_id WHERE card_id = ?""", (card_id,))
    conn.commit()
    sets = cursor.fetchall()
    return sets

def write_collection_to_csv(collection_data):
    """
    Write collection data to a CSV file.
    :param collection_data: List of tuples containing collection data.
    """

    with open("collection_data.csv", mode = "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Card Name","Count"])
        writer.writerows(collection_data)

def find_missing_cards(desired_copies):
    """
    Find cards where the total count is below the desired number of copies.
    :param desired_copies: Minimum number of copies required.
    :return: List of tuples containing missing card data.
    """
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

    return missing_cards

def required_sets(missing_cards, desired_copies=3):
    """
    Determine the sets needed to obtain missing cards.
    :param missing_cards: List of missing card data.
    :param desired_copies: Number of copies required per card.
    :return: Dictionary mapping set_id to (set_name, sets_needed).
    """
    conn = connect_db()
    cursor = conn.cursor()

    card_set_map = defaultdict(list) 

    for _, current_count, card_id in missing_cards:
        cursor.execute("""
                        SELECT sets.set_id, sets.set_name, sets_cards.card_count
                        FROM sets_cards
                        JOIN sets ON sets_cards.set_id = sets.set_id
                        WHERE sets_cards.card_id = ?""", (card_id,))
        
        sets_with_card = cursor.fetchall()
        
        for set_id, set_name, card_count in sets_with_card:
            if card_count > 0:
                copies_needed = max(0, (desired_copies - current_count))
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
    """
    Retrieve all sets that contain a specific card.
    :param card_id: ID of the card.
    :return: List of tuples containing set data.
    """
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
    """
    Retrieve the image path of a card given its name.
    :param card_name: Name of the card.
    :return: Path to the card image.
    """
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
    
def get_set_count_from_collections(set_id):
    """
    Retrieve the quantity of a specific set owned in the collection.
    :param set_id: ID of the set.
    :return: Quantity owned.
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
                    SELECT quantity_owned
                    FROM collection
                    WHERE set_id = ?
                  """, (set_id,)
                  )
    
    set_count = cursor.fetchone()[0]

    return set_count