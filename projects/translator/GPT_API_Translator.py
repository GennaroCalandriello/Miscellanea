import openai
from openai import OpenAI
import fitz
from dotenv import load_dotenv
from tqdm import tqdm
import os
import requests


# load enviroment variables
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
my_api_key = os.getenv("OPENAI_API_KEY")
start_page = int(os.getenv("START_PAGE"))
end_page = int(os.getenv("END_PAGE"))
path_book1 = "RelaxationStudies.pdf"
path_book2 = "C_Chang.pdf"
model = "gpt-4"
source_lang = "english"
target_lang = "italian"


def test_completion():
    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair.",
            },
            {
                "role": "user",
                "content": "Compose a poem that explains the concept of recursion in programming.",
            },
        ],
    )

    print(completion.choices[0].message)


def test_API():
    my_api_key = openai.api_key  # Make sure to replace this with your actual API key
    headers = {
        "Authorization": f"Bearer {my_api_key}",
    }
    payload = {
        "model": model,  # Adjust model as needed
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": "Translate the following Italian text to French: mannaggia il cuore di cristo re inappagato gigolò di strada!",
            },
        ],
        "temperature": 0.5,
        "max_tokens": 60,
    }
    response = requests.post(
        "https://api.openai.com/v1/chat/completions", json=payload, headers=headers
    )

    if response.status_code == 200:
        print("Connection to OpenAI API successful")
        print("response: ", response.json())
    else:
        print(
            f"Failed to connect to OpenAI GPT API. Status code: {response.status_code}"
        )
        print(
            "response: ", response.json()
        )  # Using response.json() for more structured error info


def translate_text(text, source_lang="English", target_lang="Italian"):
    client = openai.Client()  # Assicurati di aver configurato il client correttamente
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant. Translate and ascertain the correctness.",
                },
                {
                    "role": "user",
                    "content": f"Translate the following text from {source_lang} to {target_lang}: {text}",
                },
                {
                    "role": "system",
                    "content": "Now that you have translated the text, please check the grammar and correctness of the translation.",
                },
                {
                    "role": "user",
                    "content": "Check the grammar and correctness of the translation. In your response include only the translated text",
                },
            ],
        )
        # Estrarre il testo tradotto dalla risposta
        translated_text = response.choices[
            0
        ].message.content  # Accedere alla proprietà 'content'
        # print("Translated text:", translated_text)
        return translated_text  # Rimuovere spazi bianchi superflui
    except Exception as e:
        print(f"An error occurred during translation: {e}")
        return ""


def insert_text_in_pdf(page, text, position):
    import textwrap

    """
    Inserisce il testo in una pagina del PDF, effettuando il wrapping del testo
    per non superare la lunghezza massima specificata per riga. I parametri come
    la lunghezza massima della riga, l'altezza della linea e la dimensione del font
    sono definiti all'interno della funzione.

    Args:
        page: La pagina del PDF dove inserire il testo.
        text (str): Il testo da inserire.
        position (tuple): La posizione iniziale del testo (x, y).
    """
    # Specifica qui i valori costanti
    max_line_length = 130  # Numero massimo di caratteri per riga
    line_height = 12  # Distanza in pixel tra le righe
    fontsize = 9  # Dimensione del font del testo

    wrapped_text = textwrap.wrap(text, width=max_line_length)
    x, y = position

    for line in wrapped_text:
        # Inserisce ogni riga di testo nel documento PDF
        page.insert_text(
            (x, y),
            line,
            fontsize=fontsize,
            fontname="helv",
            fontfile=None,
            color=None,
            fill=None,
            render_mode=0,
            border_width=1,
            rotate=0,
            morph=None,
            stroke_opacity=1,
            fill_opacity=1,
            overlay=True,
            oc=0,
        )
        # Sposta la posizione y verso il basso per la prossima riga
        y += line_height


def process_pdf(
    input_pdf_path=path_book2,
    output_pdf_path="C_Chang_revisited.pdf",
):
    documento = fitz.open(input_pdf_path)
    translated_document = fitz.open()  # qui creo un documento pdf vuoto

    initial_page = 10
    final_page = 14  # numero di pagine del documento

    for page_num in range(initial_page, final_page):
        page = documento.load_page(page_num)
        text = page.get_text("text")
        translated_text = translate_text(text)

        # qui creo una nuova pagina nel documento vuoto con la stessa dimensione dell'originale
        new_page = translated_document.new_page(
            width=page.rect.width, height=page.rect.height
        )
        # Ensure translated_text is a string before inserting
        if isinstance(translated_text, str):

            insert_text_in_pdf(new_page, translated_text, position=(50, 50))

            # new_page.insert_text(
            #     (20, 30),
            #     translated_text,
            #     fontsize=8.5,
            #     fontname="helv",
            #     fontfile=None,
            #     color=None,
            #     fill=None,
            #     render_mode=0,
            #     border_width=1,
            #     rotate=0,
            #     morph=None,
            #     stroke_opacity=1,
            #     fill_opacity=1,
            #     overlay=True,
            #     oc=0,
            # ) #----------
            print("Translated and inserted text successfully.")
        else:
            print("Translated text is not in string format.")

    translated_document.save(output_pdf_path)
    translated_document.close()
    documento.close()

    return output_pdf_path


if __name__ == "__main__":
    process_pdf()
