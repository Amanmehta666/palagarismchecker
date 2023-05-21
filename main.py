import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import telebot

# Initialize your Telegram bot using your bot token
bot = telebot.TeleBot('1022661921:AAFSCX73U3iNoRlNTVKbM5RumEuu4pQQ8lY')


def vectorize(Text): return TfidfVectorizer().fit_transform(Text).toarray()
def similarity(doc1, doc2): return cosine_similarity([doc1, doc2])


def check_plagiarism_and_send():
    student_files = [doc for doc in os.listdir() if doc.endswith('.txt')]
    student_notes = [open(_file, encoding='utf-8').read() for _file in student_files]

    vectors = vectorize(student_notes)
    s_vectors = list(zip(student_files, vectors))

    plagiarism_results = set()

    for student_a, text_vector_a in s_vectors:
        new_vectors = s_vectors.copy()
        current_index = new_vectors.index((student_a, text_vector_a))
        del new_vectors[current_index]
        for student_b, text_vector_b in new_vectors:
            sim_score = similarity(text_vector_a, text_vector_b)[0][1]
            student_pair = sorted((student_a, student_b))
            score = (student_pair[0], student_pair[1], sim_score)
            plagiarism_results.add(score)

    if plagiarism_results:
        message = "Plagiarism detected:\n\n"
        for data in plagiarism_results:
            message += f"{data[0]} and {data[1]} with similarity score: {data[2]}\n"
        bot.send_message('@EducasJOBS', message)
    else:
        bot.send_message('@EducasJOBS', "No plagiarism detected.")


# Call the function to check plagiarism and send results to Telegram channel
check_plagiarism_and_send()
