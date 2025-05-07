import csv
import os

# Chemin absolu vers ton CSV
CSV_PATH = r'C:\Users\ac75009559\Desktop\AcossDev\FrontTest\projet droit ia v2\backend\db\conversations.csv'

def get_conversations_by_user(user_id):
    conversations = []
    with open(CSV_PATH, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # skip header
        for row in reader:
            if len(row) < 5:
                continue  # skip lignes incomplètes
            if row[1] != str(user_id):
                continue
            conversations.append({
                'id': row[0],
                'title': row[2],
                'date': row[4],
            })
    return conversations


def add_conversation(user_id, title, message, date):
    # Calculer nouvel id en lisant les ids existants
    last_id = 0
    with open(CSV_PATH, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # skip header
        for row in reader:
            if row and row[0].isdigit():
                last_id = max(last_id, int(row[0]))

    new_id = last_id + 1

    with open(CSV_PATH, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([new_id, user_id, title, message, date])


def get_all_conversations():
    conversations = []
    with open(CSV_PATH, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # skip header
        for row in reader:
            if len(row) < 5:
                continue
            conversations.append({
                'id': row[0],
                'user_id': row[1],
                'title': row[2],
                'message': row[3],
                'date': row[4],
            })
    return conversations
