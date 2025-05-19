
#crud.py



import csv
import os
from collections import defaultdict

BASE_DIR = os.path.dirname(__file__)
CSV_PATH = os.path.join(BASE_DIR, 'conversations.csv')

def get_conversations_by_user(user_id: int):
    grouped = defaultdict(list)
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            if len(row) < 5 or row[1] != str(user_id):
                continue
            grouped[row[2]].append({
                'id': row[0], 'user_id': row[1],
                'title': row[2], 'message': row[3], 'date': row[4]
            })
    return [msgs[0] for msgs in grouped.values()]

def add_conversation(user_id, title, message, date):
    last_id = 0
    if os.path.exists(CSV_PATH):
        with open(CSV_PATH, 'r', encoding='utf-8') as f:
            for row in csv.reader(f):
                if row and row[0].isdigit():
                    last_id = max(last_id, int(row[0]))
    new_id = last_id + 1

    # Crée le fichier et l'en-tête si nécessaire
    header = not os.path.exists(CSV_PATH) or os.stat(CSV_PATH).st_size == 0
    with open(CSV_PATH, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if header:
            writer.writerow(['id','user_id','title','message','date'])
        writer.writerow([new_id, user_id, title, message, date])
    return {"id": new_id, "user_id": user_id, "title": title, "message": message, "date": date}

def add_message(user_id: int, title: str, message: str, timestamp: str):
    last_id = 0
    try:
        with open(CSV_PATH, 'r', encoding='utf-8') as f:
            for row in csv.reader(f):
                if row and row[0].isdigit():
                    last_id = int(row[0])
    except FileNotFoundError:
        pass

    new_id = last_id + 1
    with open(CSV_PATH, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([new_id, user_id, title, message, timestamp])

def get_messages_by_conversation_title(user_id: int, conversation_title: str):
    msgs = []
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if int(row["user_id"]) == user_id and row["title"].strip() == conversation_title.strip():
                msgs.append({
                    "user_id": int(row["user_id"]),
                    "title": row["title"],
                    "message": row["message"],
                    "date": row["date"]
                })
    return msgs

def delete_conversation_by_title(title: str):
    updated, found = [], False
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            if row['title'] != title:
                updated.append(row)
            else:
                found = True
    if not found:
        return False
    with open(CSV_PATH, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["id","user_id","title","message","date"])
        writer.writeheader()
        writer.writerows(updated)
    return True
