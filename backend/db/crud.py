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
        writer.writerow([new_id, user_id, title, message, date])
    
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


def add_message(conversation_id, message, response, timestamp):
    with open(CSV_PATH, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([conversation_id, message, response, timestamp])  # Ajout des messages dans le CSV
