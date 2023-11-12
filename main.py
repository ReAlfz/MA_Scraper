import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer


# create dataset from scraping
def create_dataset():
    data = pd.read_csv('putusan/putusan_ma_narkotika_2023-11-09.csv')

    data['Barang Bukti'] = data['catatan_amar'].apply(
        lambda x: x[x.lower().find("barang bukti"):x.lower().find("dirampas untuk dimusnahkan")]
    )
    df = data[['nomor', 'lembaga_peradilan', 'Barang Bukti', 'catatan_amar']]
    print(df.head(5))

    df = df.rename(columns={
        'nomor': 'No Putusan',
        'lembaga_peradilan': 'Lembaga Peradilan',
        'Barang Bukti': 'Barang Bukti',
        'catatan_amar': 'Amar Putusan'
    })

    df.to_csv('putusan/putusan_ma_narkotika_2023-11-09_cleaned_text.csv')


def preprocess_text(text):
    words = word_tokenize(text)

    stop_words = set(stopwords.words('indonesian'))
    words = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]
    ps = PorterStemmer()
    words = [ps.stem(word) for word in words]

    return ' '.join(words)


def euclidean_distance(vec1, vec2):
    if len(vec1) != len(vec2):
        raise ValueError("Vectors must have the same length")

    # Calculate the Euclidean Distance
    distance = np.linalg.norm(np.array(vec1) - np.array(vec2))
    return distance


def search_euclidean(query, document_index):
    preprocessed_query = preprocess_text(query)

    # Create a set of words common to both query and documents
    common_words = set(preprocessed_query.split())
    for doc_text in document_index.values():
        common_words |= set(doc_text.split())

    # Create vectors for the query and each document based on the common vocabulary
    query_vector = [preprocessed_query.split().count(word) for word in common_words]

    distances = {}
    for doc_id, doc_text in document_index.items():
        doc_vector = [doc_text.split().count(word) for word in common_words]
        distance = euclidean_distance(query_vector, doc_vector)
        distances[doc_id] = distance

    # Sort the results by distance in ascending order
    sorted_results = sorted(distances.items(), key=lambda x: x[1])

    return sorted_results


if __name__ == '__main__':
    data = pd.read_csv('putusan/putusan_ma_narkotika_2023-11-09_cleaned_text.csv')
    text = data['Amar Putusan'].apply(preprocess_text)
    document_index = dict(zip(data['No Putusan'], text))

    query = input("Enter your query: ")
    results = search_euclidean(query, document_index)

    for result in results[:10]:
        doc_id, score = result
        print(f"Document ID: {doc_id}, Score: {score}")
        print(data.loc[data['No Putusan'] == doc_id, 'Amar Putusan'].values[0])
        print("\n---\n")
