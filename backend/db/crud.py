
#crud.py



import csv
import os
from collections import defaultdict
# Chemin absolu vers ton CSV
CSV_PATH = r'/Users/clementgardair/Desktop/AcossDev/TheLawyer/backend/db/conversations.csv'

def get_conversations_by_user_title(user_id: int, conversation_title: str):
    """
    Récupère les messages d'une conversation spécifique pour un utilisateur donné
    en filtrant par titre et id utilisateur.
    """
    messages = []
    
    with open("db/conversations.csv", newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            try:
                if int(row["user_id"]) == user_id and str(row["title"]).strip() == conversation_title.strip():
                    messages.append({
                        "user_id": int(row["user_id"]),
                        "title": row["title"],
                        "message": row["message"],
                        "date": row["date"]
                    })
            except (ValueError, KeyError):
                continue  # Ignore les lignes corrompues ou incomplètes
    
    return messages

def get_conversations_by_user(user_id):
    # Créer un dictionnaire pour regrouper les conversations par titre
    grouped_conversations = defaultdict(list)
    
    with open(CSV_PATH, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        for row in reader:
            if len(row) < 5:
                continue  # Skip incomplete rows
            if row[1] != str(user_id):
                continue  # Filter by user_id
            # Ajouter la ligne au groupe correspondant au titre
            grouped_conversations[row[2]].append({
                'id': row[0],
                'user_id': row[1],
                'title': row[2],
                'message': row[3],
                'date': row[4],
            })
    
    # Créer l'historique en ne gardant que la première ligne de chaque groupe
    conversation_history = []
    for title, messages in grouped_conversations.items():
        # Ajouter la première ligne de chaque groupe (premier message pour ce titre)
        conversation_history.append(messages[0])  # messages[0] étant la première ligne du groupe
    
    return conversation_history


def add_conversation(user_id,title, message, date):
    # Calculer le nouvel id en lisant les ids existants
    last_id = 0
    
    # Si le fichier CSV existe déjà, lire les IDs existants
    if os.path.exists(CSV_PATH):
        with open(CSV_PATH, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Sauter l'en-tête
            for row in reader:
                if row and row[0].isdigit():  # Vérifier que l'ID est un chiffre
                    last_id = max(last_id, int(row[0]))  # Récupérer le dernier ID

    # Calculer le nouvel ID
    new_id = last_id + 1  # Nouveau ID

    # Ajouter la nouvelle conversation dans le fichier CSV
    with open(CSV_PATH, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Si le fichier est vide, ajouter l'en-tête
        if os.stat(CSV_PATH).st_size == 0:
            writer.writerow(['id', 'user_id', 'title', 'message', 'date'])  # En-tête si fichier vide
        
        # Ajouter la nouvelle ligne (conversation) dans le fichier CSV
        writer.writerow([new_id,user_id,title,message,date])
    
    return {"id": new_id, "user_id": user_id, "title": title, "message": message, "date": date}
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


def add_message(user_id: int, title: str, message: str, timestamp: str):
    # Lire les lignes du fichier CSV pour obtenir le dernier ID
    last_id = 0
    try:
        with open(CSV_PATH, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)  # ⬅️ Ignorer l'en-tête
            for row in reader:
                if row and row[0].isdigit():
                    last_id = int(row[0])
    except FileNotFoundError:
        pass

    new_id = last_id + 1
    print("erreur2")
    # Ajouter le message dans le fichier CSV avec un nouvel ID
    with open(CSV_PATH, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([new_id, user_id, title, message, timestamp])
        
def get_messages_by_conversation_title(user_id: int, conversation_title: str):
    messages = []
    with open("db/conversations.csv", newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if (
                str(row["title"]).strip() == conversation_title.strip() and
                int(row["user_id"]) == user_id
            ):
                messages.append({
                    "user_id": int(row["user_id"]),
                    "title": row["title"],
                    "message": row["message"],
                    "date": row["date"]
                })
    return messages



def delete_conversation_by_title(title: str):
    updated_rows = []
    deleted = False

    with open("db/conversations.csv", newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['title'] != title:
                updated_rows.append(row)
            else:
                deleted = True

    if not deleted:
        return False  # Aucune conversation avec ce titre

    with open("db/conversations.csv", mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["id", "user_id", "title", "message", "date"])
        writer.writeheader()
        writer.writerows(updated_rows)

    return True