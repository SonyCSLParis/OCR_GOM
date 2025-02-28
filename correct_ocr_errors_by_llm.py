from utils import get_file_content, get_json_file_content, write_content_in_file, string_contains_digit
from correct_words_by_llm import retrieve_llm_corrected_words
from generate_ocr_books_scores import generate_pairwise_score
import unicodedata
import spacy

def normalize_words(text):
    return unicodedata.normalize('NFC', text)

def put_error_in_list(error_list, error, error_sentence, sentence_index):
        for error_in_list in error_list:
                if error_in_list[0] == error:
                        error_in_list[2] += 1
                        return error_list
        return error_list.append([error, error_sentence, 0, sentence_index])

def is_in_dictionary(searched_word, dictionary):
        dictionary = dictionary.split("\n")
        for dictionary_word in dictionary:
                if (dictionary_word == searched_word):
                        return True, searched_word
        return False, searched_word

def compound_word_is_in_word_dictionary(word, dictionary):
        compound_word = word.split('-')
        if (len(compound_word) == 1):
                return False, word
        for part_compound_word in compound_word:
                result = is_in_dictionary(part_compound_word, dictionary)
                if (result[0] == False):
                        return False, word
        return True, word

def is_in_one_dictionary(token_text):
        result = is_in_dictionary(token_text.lower(), morphalou_dictionary)
        if (result[0] == True):
            return result
        result = is_in_dictionary(token_text, french_cities_dictionary)
        if (result[0] == True):
            return result
        result = is_in_dictionary(token_text, countries_dictionary)
        if (result[0] == True):
            return result
        return compound_word_is_in_word_dictionary(token_text.lower(), morphalou_dictionary)

def retrieve_ocr_errors(ocr_sentences):
        ocr_errors = []
        for index, ocr_sentence in enumerate(ocr_sentences):
                for token in ocr_sentence:
                        if token.is_punct == False:
                                if (string_contains_digit(token.text)):
                                        continue
                                result = is_in_one_dictionary(token.text)
                                if (result[0] == False):
                                        put_error_in_list(ocr_errors, token.text, ocr_sentence, index)
        return ocr_errors

def retrieve_ocr_errors_with_context(ocr_errors):
        ocr_errors_with_context = ""
        nb_ocr_errors_with_context = 0
        for ocr_error in ocr_errors:
                if ocr_error[2] == 0:
                        ocr_errors_with_context += str(ocr_error[0]) + " | " + str(ocr_error[1]) + "\n"
                        nb_ocr_errors_with_context += 1
        return ocr_errors_with_context, nb_ocr_errors_with_context

def correct_ocr_errors_in_text(ocr_text, ocr_errors, corrected_words):
        corrected_word_index = 0
        for ocr_error in ocr_errors:
                if ocr_error[2] != 0:
                        continue
                ocr_text = ocr_text.replace(ocr_error[0], corrected_words[corrected_word_index].lstrip())
                corrected_word_index += 1
        return ocr_text

expected_text = get_file_content("data/results/pages_concatenate/expected_results_txt/L_école_du_jardin_potager/L_école_du_jardin_potager.txt")
ocr_text = get_file_content("data/results/pages_concatenate/kraken_results_txt/L_école_du_jardin_potager/L_école_du_jardin_potager.txt")
french_cities_dictionary = get_file_content("data/dictionary/french_cities.txt")
countries_dictionary = get_file_content("data/dictionary/countries.txt")
morphalou_dictionary = get_file_content("data/dictionary/morphalou.txt")

nlp = spacy.load("fr_dep_news_trf")
expected_text = normalize_words(expected_text)
ocr_text = normalize_words(ocr_text)
ocr_sentences = [i for i in nlp(ocr_text).sents]

ocr_errors = retrieve_ocr_errors(ocr_sentences)
ocr_errors_with_context, nb_ocr_errors_with_context = retrieve_ocr_errors_with_context(ocr_errors)
corrected_words = retrieve_llm_corrected_words(ocr_errors_with_context, nb_ocr_errors_with_context, "mistral")
corrected_text = correct_ocr_errors_in_text(ocr_text, ocr_errors, corrected_words)
write_content_in_file("data/results/pages_concatenate/mistral_corrected_results_txt/L_école_du_jardin_potager/L_école_du_jardin_potager.txt", corrected_text, 'w')

kraken_score = generate_pairwise_score(expected_text, ocr_text)
corrected_kraken_score = generate_pairwise_score(expected_text, corrected_text)
print("kraken similarity score:", kraken_score, "out of 1.0.")
print("corrected kraken similarity score:", corrected_kraken_score, "out of 1.0.")