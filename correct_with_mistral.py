import os
from mistralai import Mistral
from utils import get_file_content

def correct_with_mistral(ocr_errors_with_context, model):
    instructions = "Voici une liste de mots potentiellement mal orthographiés car absents du dictionnaire français que j’utilise. Pour chaque mot, sa phrase d'origine est fournie. Ces phrases proviennent de livres sur le maraîchage français au XIXe siècle, traitées par OCR. Liste uniquement les mots corrigés, sans explication."
    client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])

    chat_response = client.chat.complete(
        model = model,
        messages = [
            {
                "role": "user",
                "content": instructions + ocr_errors_with_context,
            },
        ]
    )
    return chat_response.choices[0].message.content

def retrieve_mistral_corrected_words(ocr_errors_with_context, nb_ocr_errors_with_context):
    corrected_ocr_errors = []
    while nb_ocr_errors_with_context != len(corrected_ocr_errors):
            mistral_corrected_ocr_errors_response = correct_with_mistral(ocr_errors_with_context, "mistral-large-latest")
            corrected_ocr_errors = mistral_corrected_ocr_errors_response.split("\n")
    return corrected_ocr_errors
