"""Defines all the functions related to the database"""

from app import db
from datetime import datetime
import random

def fetch_listing(checkin, checkout, num_guest) -> dict:
    """Reads all tasks listed in the todo table

    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    query = 'SELECT listing_id, price, D.description, D.room_type, D.property_type, D.bedrooms, D.beds, D.picture_url \
        FROM (SELECT listing_id, AVG(price) price FROM calendar WHERE date >= "{}" AND date < "{}" AND available = 1 \
            GROUP BY listing_id HAVING COUNT(listing_id) >= datediff( "{}" , "{}") ) AS available \
        NATURAL JOIN (SELECT * FROM description WHERE beds BETWEEN {}-1 AND {}+1) AS D;'.format(checkin, checkout, checkout, checkin, num_guest, num_guest)
    query_results = conn.execute(query).fetchall()
    conn.close()
    available_list = []
    for result in query_results:
        item = {
            "listing_id": result[0],
            "price": float(result[1]),
            "description": result[2],
            "room_type": result[3],
            "property_type": result[4],
            "bedrooms": result[5],
            "beds": result[6],
            "picture_url": result[7],
        }
        available_list.append(item)
    conn.close()
    return available_list


def add_reviews(listing_id,reviewer_id, reviewer_name, comment):

    
    date = datetime.today().strftime('%Y-%m-%d')
    conn = db.connect()
    review_id_list = conn.execute("SELECT review_id FROM review ORDER BY review_id DESC").fetchall()
    review_id_list = [x[-1] for x in review_id_list] 

    while(1):
        new_review_id = random.randint(1,review_id_list[0]+1)
        if new_review_id not in review_id_list:
            query = 'INSERT INTO review VALUES ( "{}" , "{}", "{}" , "{}" ,"{}" , "{}")'.format(listing_id,new_review_id,date, reviewer_id, reviewer_name, comment)
            break

    conn.execute(query)

    query = 'SELECT * FROM review WHERE review_id = "{}";'.format(new_review_id)
    query_results = conn.execute(query).fetchall()
    result = {"listing_id": query_results[0][0], "review_id": int(query_results[0][1]),"date": str(query_results[0][2]),
    "reviewer_id": int(query_results[0][3]), "reviewer_name": query_results[0][4], "comment": query_results[0][5]}
    conn.close()
    return result


def delete_reviews(review_id):
    """Delete comment

    """
    conn = db.connect()
    query = 'DELETE FROM review WHERE review_id = "{}"'.format(review_id)
    conn.execute(query)
    conn.close()

def update_reviews(review_id, new_comment):
    conn = db.connect()
    date = datetime.today().strftime('%Y-%m-%d')

    query = 'UPDATE review SET comments = "{}", date = "{}" WHERE review_id = "{}";'.format(new_comment, date ,review_id)
    conn.execute(query)
    conn.close()


# def lookup_reviews(review_id):
#     conn = db.connect()
#     query = 'SELECT * FROM review WHERE review_id = "{}"'.format(new_comment, review_id)
#     query_results = conn.execute(query).fetchall()
#     review_list = []
#     for result in query_results:
#         item = {
#             "listing_id": result[0],
#             "review_id": result[1],
#             "date": result[2],
#             "reviewer_id": result[3],
#             "reviewer_name": result[4],
#             "comment": result[5]
#         }
#         review_list.append(item)
#     conn.close()
#     return review_list

def fetch_reviews(reviewer_id, reviewer_name):
    conn = db.connect()
    query = 'SELECT * FROM review WHERE reviewer_id = "{}" AND reviewer_name = "{}" '.format(reviewer_id, reviewer_name)
    query_results = conn.execute(query).fetchall()
    review_list = []
    for result in query_results:
        item = {
            "listing_id": result[0],
            "review_id": int(result[1]),
            "date": str(result[2]),
            "reviewer_id": int(result[3]),
            "reviewer_name": result[4],
            "comment": result[5]
        }
        review_list.append(item)
    conn.close()
    return review_list

# def update_task_entry(task_id: int, text: str) -> None:
#     """Updates task description based on given `task_id`

#     Args:
#         task_id (int): Targeted task_id
#         text (str): Updated description

#     Returns:
#         None
#     """

#     conn = db.connect()
#     query = 'Update tasks set task = "{}" where id = {};'.format(text, task_id)
#     conn.execute(query)
#     conn.close()


# def update_status_entry(task_id: int, text: str) -> None:
#     """Updates task status based on given `task_id`

#     Args:
#         task_id (int): Targeted task_id
#         text (str): Updated status

#     Returns:
#         None
#     """

#     conn = db.connect()
#     query = 'Update tasks set status = "{}" where id = {};'.format(text, task_id)
#     conn.execute(query)
#     conn.close()


# def insert_new_task(text: str) ->  int:
#     """Insert new task to todo table.

#     Args:
#         text (str): Task description

#     Returns: The task ID for the inserted entry
#     """

#     conn = db.connect()
#     query = 'Insert Into tasks (task, status) VALUES ("{}", "{}");'.format(
#         text, "Todo")
#     conn.execute(query)
#     query_results = conn.execute("Select LAST_INSERT_ID();")
#     query_results = [x for x in query_results]
#     task_id = query_results[0][0]
#     conn.close()

#     return task_id


# def remove_task_by_id(task_id: int) -> None:
#     """ remove entries based on task ID """
#     conn = db.connect()
#     query = 'Delete From tasks where id={};'.format(task_id)
#     conn.execute(query)
#     conn.close()
