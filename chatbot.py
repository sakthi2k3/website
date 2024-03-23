# chatbot.py

import spacy
import pandas as pd
from PyDictionary import PyDictionary
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from difflib import SequenceMatcher
import re

# Load the English language model
nlp = spacy.load("en_core_web_sm")

# Step 1: Preprocessing the Data
df = pd.read_csv("medicine_dataset.csv", encoding='latin-1')
df.fillna("None", inplace=True)

# Step 2: Vectorize Text Data
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['name'] + ' ' + df['substitute0'] + ' ' + df['substitute1'] + ' ' + df['substitute2'] + ' ' + df['substitute3'] + ' ' + df['substitute4'] + ' ' + df['sideEffect0'] + ' ' + df['sideEffect1'] + ' ' + df['sideEffect2'] + ' ' + df['sideEffect3'] + ' ' + df['sideEffect4'] + ' ' + df['sideEffect5'] + ' ' + df['sideEffect6'] + ' ' + df['sideEffect7'] + ' ' + df['sideEffect8'] + ' ' + df['sideEffect9'] + ' ' + df['sideEffect10'] + ' ' + df['sideEffect11'] + ' ' + df['sideEffect12'] + ' ' + df['sideEffect13'] + ' ' + df['sideEffect14'] + ' ' + df['sideEffect15'] + ' ' + df['sideEffect16'] + ' ' + df['sideEffect17'] + ' ' + df['sideEffect18'] + ' ' + df['sideEffect19'] + ' ' + df['sideEffect20'] + ' ' + df['sideEffect21'] + ' ' + df['sideEffect22'] + ' ' + df['sideEffect23'] + ' ' + df['sideEffect24'] + ' ' + df['sideEffect25'] + ' ' + df['sideEffect26'] + ' ' + df['sideEffect27'] + ' ' + df['sideEffect28'] + ' ' + df['sideEffect29'] + ' ' + df['sideEffect30'] + ' ' + df['sideEffect31'] + ' ' + df['sideEffect32'] + ' ' + df['sideEffect33'] + ' ' + df['sideEffect34'] + ' ' + df['sideEffect35'] + ' ' + df['sideEffect36'] + ' ' + df['sideEffect37'] + ' ' + df['sideEffect38'] + ' ' + df['sideEffect39'] + ' ' + df['sideEffect40'] + ' ' + df['sideEffect41'] + ' ' + df['use0'] + ' ' + df['use1'] + ' ' + df['use2'] + ' ' + df['use3'] + ' ' + df['use4'] + ' ' + df['Chemical Class'] + ' ' + df['Habit Forming'] + ' ' + df['Therapeutic Class'] + ' ' + df['Action Class'])


# similar
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def find_closest_match(query, dataset, threshold=0.7):
    closest_match = None
    max_similarity = 0
    print("searching closest_match for", query)
    for name in dataset:
        similarity = similar(query.lower(), name.lower())
        if similarity > max_similarity and similarity >= threshold:
            max_similarity = similarity
            closest_match = name

    return closest_match


def chat_with_bot1(query):
    matched_medicine = find_closest_match(query, df['name'].tolist())

    # If no close match is found, return None
    if matched_medicine is None:
        return None

    # Retrieve information about the matched medicine
    medicine_info = df[df['name'] == matched_medicine].iloc[0]

    return {
        'medicine': medicine_info['name'],
        'substitute': [medicine_info[f'substitute{i}'] for i in range(5) if
                       medicine_info[f'substitute{i}'] != 'None'],
        'side_effects': [medicine_info[f'sideEffect{i}'] for i in range(42) if
                         medicine_info[f'sideEffect{i}'] != 'None'],
        'uses': [medicine_info[f'use{i}'] for i in range(5) if medicine_info[f'use{i}'] != 'None'],
        'chemical_class': medicine_info['Chemical Class'],
        'habit_forming': medicine_info['Habit Forming'],
        'therapeutic_class': medicine_info['Therapeutic Class'],
        'action_class': medicine_info['Action Class']
    }

# Step 3: Chat with the Bot
def chat_with_bot(query):
    query_vector = vectorizer.transform([query])
    similarity_scores = cosine_similarity(query_vector, X)
    most_similar_index = similarity_scores.argmax()
    medicine_info = df.iloc[most_similar_index]
    if medicine_info['name'] == '#':
        return chat_with_bot1(query)
    else:
        return {
            'medicine': medicine_info['name'],
            'substitute': [medicine_info[f'substitute{i}'] for i in range(5) if medicine_info[f'substitute{i}'] != 'None'],
            'side_effects': [medicine_info[f'sideEffect{i}'] for i in range(42) if medicine_info[f'sideEffect{i}'] != 'None'],
            'uses': [medicine_info[f'use{i}'] for i in range(5) if medicine_info[f'use{i}'] != 'None'],
            'chemical_class': medicine_info['Chemical Class'],
            'habit_forming': medicine_info['Habit Forming'],
            'therapeutic_class': medicine_info['Therapeutic Class'],
            'action_class': medicine_info['Action Class']
        }

def extract_medicine_name(query):
    # Initialize PyDictionary
    dictionary = PyDictionary()

    # Process the user query
    doc = nlp(query)

    # Define patterns for medicine name extraction
    patterns = ["side effects of","side effects for","side effect of","side effect for", "uses for","use of","uses of","use for", "substitutes for","substitute for","substitutes of","substitute of", "alternatives for","alternative for","alternatives of","alternative of", "info about"]

    # Check if any pattern is present in the query
    for pattern in patterns:
        if pattern in query:
            medicine_name = query.split(pattern)[-1].strip()
            return medicine_name

        # If no pattern is found, check for individual medicine names in the query
    tokens_of_interest = [token.text for token in doc if not token.is_punct and not token.is_stop and not token.is_space]

    for token in tokens_of_interest:
        if not dictionary.meaning(token):
            medicine_name = token
            break
    return medicine_name


def extract_medicine_names(query):
    # Initialize PyDictionary
    dictionary = PyDictionary()

    # Process the user query
    doc = nlp(query)

    # Split the query by 'and' or ','
    split_query = re.split(r'\s+and\s+|,\s*', query)
    medicine_names = []
    for part in split_query:
        tokens_of_interest = [token.text for token in nlp(part) if not token.is_punct and not token.is_stop and not token.is_space]

        for token in tokens_of_interest:
            if not dictionary.meaning(token):
                medicine_names.append(token)
    return split_query


if __name__ == "__main__":
    while True:
        query = input("You:")
        if "bye" in query or "exit" in query:
            print("Goodbye, have a nice day!")
            break

        # Extract a single medicine name using extract_medicine_name
        medicine_name = extract_medicine_name(query)

        # If 'and' or ',' is present, use extract_medicine_names
        if ' and ' in medicine_name or ',' in medicine_name:
            medicine_names = extract_medicine_names(medicine_name)

            if medicine_names:
                for medicine_name in medicine_names:
                    response = chat_with_bot(medicine_name)

                    if not response:
                        print(f"Could not extract medicine name from the query: {medicine_name}")
                    else:
                        if "side effects" in query or "side effect" in query:
                            s = "Side Effects of " + response['medicine'] + ": "
                            side_effects = ', '.join(response['side_effects'])
                            print(s + side_effects)

                        if "substitutes" in query or "substitute" in query or "alternative" in query:
                            s = "Alternative medicines for " + response['medicine'] + ": "
                            substitutes = ', '.join(response['substitute'])
                            print(s + substitutes)

                        if "use" in query or "uses" in query:
                            s = response['medicine'] + " is commonly used for: "
                            uses = ', '.join(response['uses'])
                            print(s + uses)
            else:
                print("Could not extract medicine names from the query.")
        else:
            # If no 'and' or ',' is present, proceed with single medicine name
            if medicine_name:
                response = chat_with_bot(medicine_name)
                if response:
                    if "side effects" in query or "side effect" in query:
                        s = "Side Effects of " + response['medicine'] + ": "
                        side_effects = ', '.join(response['side_effects'])
                        print(s + side_effects)

                    if "substitutes" in query or "substitute" in query or "alternative" in query:
                        s = "Alternative medicines for " + response['medicine'] + ": "
                        substitutes = ', '.join(response['substitute'])
                        print(s + substitutes)

                    if "use" in query or "uses" in query:
                        s = response['medicine'] + " is commonly used for: "
                        uses = ', '.join(response['uses'])
                        print(s + uses)
            else:
                print("Could not extract medicine name from the query.")

