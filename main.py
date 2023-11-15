import pandas as pd
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import euclidean_distances


def tokenize_text(text, tokenizer_):
    return tokenizer_.encode(text, add_special_tokens=True)


def embed_text(text, tokenizer_, model_):
    inputs = tokenizer_(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
    outputs = model_(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().detach().numpy()


def calculate_similarity(query1, query2, tokenizer_, model_):
    embedding1 = embed_text(query1, tokenizer_, model_)
    embedding2 = embed_text(query2, tokenizer_, model_)
    return euclidean_distances([embedding1], [embedding2])[0][0]


def create_models(data, tokenizer_, model_):
    data['tokenized_text'] = data['Amar Putusan'].apply(
        lambda x: tokenize_text(x, tokenizer_)
    )

    data['embeddings'] = data['Amar Putusan'].apply(
        lambda x: embed_text(x, tokenizer_, model_)
    )

    model.save_pretrained('bert_model')
    data.to_pickle('processed_data.pkl')


if __name__ == '__main__':
    df = pd.read_csv('putusan/putusan_ma_narkotika_2023-11-09_cleaned_text.csv')
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')
    create_models(df, tokenizer, model)

    loaded_model = BertModel.from_pretrained('bert_model')
    loaded_df = pd.read_pickle('processed_data.pkl')

    query = str(input('Search Query: '))
    query_embedding = embed_text(query, tokenizer, model)

    loaded_df['similarity'] = loaded_df['embeddings'].apply(lambda x: euclidean_distances([query_embedding], [x])[0][0])
    top_results = loaded_df.nlargest(5, 'similarity')[['No Putusan', 'Amar Putusan']]
    print(top_results)