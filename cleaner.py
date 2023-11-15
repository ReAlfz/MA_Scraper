import pandas as pd
from PyPDF4 import PdfFileReader, PdfFileWriter
from PyPDF4.pdf import ContentStream
from PyPDF4.generic import TextStringObject, NameObject
from PyPDF4.utils import b_


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


def remove_watermark(watermark, input_file, output_file):
    with open(input_file, "rb") as f:
        source = PdfFileReader(f, "rb")
        output = PdfFileWriter()

        for page in range(source.getNumPages()):
            page = source.getPage(page)
            content_object = page["/Contents"].getObject()
            content = ContentStream(content_object, source)

            for operands, operator in content.operations:
                if operator == b_("Tj"):
                    text = operands[0]

                    if isinstance(text, str) and text.startswith(watermark):
                        operands[0] = TextStringObject('')

            page.__setitem__(NameObject('/Contents'), content)
            output.addPage(page)

        with open(output_file, "wb") as outputStream:
            output.write(outputStream)