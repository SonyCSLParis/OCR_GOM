from utils import get_file_content, get_json_file_content, write_content_in_file, string_contains_digit
import unicodedata
import spacy

def normalize_words(text):
    return unicodedata.normalize('NFC', text)

def put_error_in_list(error_list, error, erorr_sentence):
        for error_in_list in error_list:
                if error_in_list[0] == error:
                        error_in_list[2] += 1
                        return error_list
        return error_list.append([error, erorr_sentence, 0])

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

def retrieve_kraken_errors(kraken_sentences):
        kraken_errors = []
        for index, kraken_sentence in enumerate(kraken_sentences):
                for token in kraken_sentence:
                        if token.is_punct == False:
                                if (string_contains_digit(token.text)):
                                        continue
                                result = is_in_one_dictionary(token.text)
                                if (result[0] == False):
                                        put_error_in_list(kraken_errors, token.text, kraken_sentence)
        return kraken_errors

def print_kraken_errors(kraken_errors):
        for error in kraken_errors:
                if error[2] == 0:
                        print(error[0], " | ", error[1])

kraken_text = get_file_content("data/results/pages_concatenate/kraken_results_txt/L_école_du_jardin_potager/L_école_du_jardin_potager.txt")
expected_text = get_file_content("data/results/pages_concatenate/expected_results_txt/L_école_du_jardin_potager/L_école_du_jardin_potager.txt")
french_words_dictionary = get_file_content("data/dictionary/fr.txt")
french_cities_dictionary = get_file_content("data/dictionary/french_cities.txt")
countries_dictionary = get_file_content("data/dictionary/countries.txt")
morphalou_dictionary = get_file_content("data/dictionary/morphalou.txt")

nlp = spacy.load("fr_dep_news_trf")
kraken_text = normalize_words(kraken_text)
kraken_sentences = [i for i in nlp(kraken_text).sents]
kraken_errors = retrieve_kraken_errors(kraken_sentences)
print_kraken_errors(kraken_errors)
