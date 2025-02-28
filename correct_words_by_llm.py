from ollama import chat, ChatResponse

instructions = "Voici une liste de mots potentiellement mal orthographiés car absents du dictionnaire français que j’utilise. Pour chaque mot, sa phrase d'origine est fournie. Ces phrases proviennent de livres sur le maraîchage français au XIXe siècle, traitées par OCR. Liste uniquement les mots corrigés, sans explication, avec le formattage suivant : nouveau mot 1\nnouveau mot 2\n"

def retrieve_llm_corrected_words(ocr_errors_with_context, nb_ocr_errors_with_context, llm_model):
    corrected_ocr_errors = []
    while nb_ocr_errors_with_context != len(corrected_ocr_errors):
        response: ChatResponse = chat(model=llm_model, messages=[{'role': 'user', 'content': instructions + ocr_errors_with_context}])
        first_llm_corrected_ocr_errors_response = response['message']['content']
        corrected_ocr_errors = first_llm_corrected_ocr_errors_response.split("\n")
    return corrected_ocr_errors
