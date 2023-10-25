import pandas as pd

if __name__ == '__main__':
    data = pd.read_csv('putusan/putusan_ma_narkotika_2023-10-25.csv')

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_colwidth', None)
    print(data.info())
    temp = [str(txt) for txt in data['text_pdf']]
    print(list(temp[:5]))