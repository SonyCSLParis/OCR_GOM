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

# ocr_errors = retrieve_ocr_errors(ocr_sentences)
ocr_errors = [
    ['cabalan', "Dès le commencement du mois, on sème aussi les choux pommés hâtifs, cœur-de-bœuf femelle, cabalan, gros-pointu de Strasbourg, pour avoir des primeurs;", 1, 3],
    ['prud’homme', "le haricot prud’homme : un mange-tout excellent peut fournir jusqu’aux gelées.", 0, 4],
    ['jusqu’', "le haricot prud’homme : un mange-tout excellent peut fournir jusqu’aux gelées.", 5, 4],
    ['d’', "On continue, d’une part, à semer et à planter tout ce qui peut être consommé ou recueilli.", 22, 6],
    ['York', "du cerfeuil, des épinards, radis jaunes-roses, navets jaunes, choux d’York, pain-de-sucre, cabus (1), cabalan, de Strasbourg (tous les choux étrangers se sément dans ce mois);", 1, 8],
    ['sément', "du cerfeuil, des épinards, radis jaunes-roses, navets jaunes, choux d’York, pain-de-sucre, cabus (1), cabalan, de Strasbourg (tous les choux étrangers se sément dans ce mois);", 1, 8],
    ['demilongs', "les petits radis roses demilongs passent assez bien les hivers;", 0, 11],
    ['annće', "Nos jardiniers sément le chou cabus plat d’été tous les mois de l'annće, pour ohtenir des primeurs ;", 0, 14],
    ['ohtenir', "Nos jardiniers sément le chou cabus plat d’été tous les mois de l'annće, pour ohtenir des primeurs ;", 0, 14],
    ['l’', "Pendant ce mois on peut semer les épinards, le cerfeuil, qui pourront donner en mars si l’automne est favorable;", 26, 18],
    ['gotte', "mais on sème avec avantage de la laitue crêpe, la laitue gotte et la laitue romaine.", 0, 19],
    ['michaux', "On sème à la fin du mois un peu de pois michaux au pied des murs, et à bonne exposition;", 1, 20],
    ['n’', "on repique le jeune chou d’York, les choux pommés semés en août, soit en pépinière, pour n’être mis en place qu’en février et mars, soit même immédiatement pour un climat tempéré.", 8, 21],
    ['qu’', "on repique le jeune chou d’York, les choux pommés semés en août, soit en pépinière, pour n’être mis en place qu’en février et mars, soit même immédiatement pour un climat tempéré.", 12, 21],
    ['c’', "c’est aussi l’époque de couper les montants d’artichaut, de nettoyer les pieds, d’en raccourcir les feuilles extérieures, de donner un labour pour faciliter le buttage que l’on fera le mois prochain.", 1, 24],
    ['sême', "On sême des radis, des laitnes, nasitort : l’as-CALENDRIER DES SEMIS.", 0, 27],
    ['laitnes', "On sême des radis, des laitnes, nasitort : l’as-CALENDRIER DES SEMIS.", 0, 27],
    ['perge', "27 perge est semée en automne avec plus de succès qu’au printemps;", 0, 28],
    ['quarantin', "le gros pois quarantin, normand à purée, à longue cosse;", 0, 29],
    ['s’', "car elle s’échauffera au printemps, et les semis et les plantations y prospèreront d’autant mieux qu’elle aura été plus divisée.", 4, 37],
    ['queCALENDRIER', "Ces cinq espèces doivent être semées par prévision, et peu, au cas de gelées trop fortes, l’observe queCALENDRIER DES SEMIS.", 0, 39],
    ['L’', "L’ÉCOLE DU JARDIN POTAGER.", 2, 41],
    ['POTAGÉRES', "CATALOGUE DES GRAINES POTAGÉRES.", 0, 43],
    ['AlL.', "AlL. Alium sativum.", 0, 44],
    ['Alium', "AlL. Alium sativum.", 0, 44],
    ['sativum', "AlL. Alium sativum.", 0, 44],
    ['Scorodoprasum', "Scorodoprasum.", 0, 47],
    ['Atriplex', "Atriplex hortensis.", 0, 51],
    ['hortensis', "Atriplex hortensis.", 0, 51],
    ['POTAGERES', "L’usage de cette30 PLANTES POTAGERES.", 1, 52],
    ['Cynara', "Cynara.", 0, 56],
    ['enPLANTES', "L’artichaut de Laon donne des produits enPLANTES POTAGÈRES.", 0, 67],
    ['officinalis', "Asparagus officinalis du midi de la France.", 0, 70],
    ['maniéres', "On multiplie l’asperge de deux maniéres, ou par le semis en place, ou bien au moyen de plants élevés en pépinière : cette dernière méthode est la plus usitée.", 0, 71],
    ['Ulm', "La graine d’asperges de Hollande verte, et grosse violette d’Ulm, sont les meilleures : on sème la graine en mars pour semis.", 0, 77],
    ['Beta', "BETTERAVE, Beta vulgaris.", 0, 78],
    ['vulgaris', "BETTERAVE, Beta vulgaris.", 0, 78],
    ['Castelnaudary', "La rouge noire et la jaune de Castelnaudary sont les plus estimées dans notre pays;", 0, 79],
    ['Ocymum', "Ocymum Basilicum.", 0, 89],
    ['Basilicum', "Ocymum Basilicum.", 0, 89],
    ['Daucus', "Daucus Carota.", 0, 92],
    ['Carota', "Daucus Carota.", 0, 92],
    ['déli', "la rouge, la blanche, déli-PLANTES POTAGERES.", 0, 97],
    ['cate', "33 cate au goût, hâtive (carotte blanche à colet vert hors terre, très-grosse : la semer claire, chaque graine à 5, 7 et 8 pouces de distance, nouvelle espèce) : les deux dernières peuvent être semées en septembre, octobre et février, pour les avoir de bonne heure, et remplacer celles qui, semées en juin, commencent à se boiser.", 0, 98],
    ['colet', "33 cate au goût, hâtive (carotte blanche à colet vert hors terre, très-grosse : la semer claire, chaque graine à 5, 7 et 8 pouces de distance, nouvelle espèce) : les deux dernières peuvent être semées en septembre, octobre et février, pour les avoir de bonne heure, et remplacer celles qui, semées en juin, commencent à se boiser.", 0, 98],
    ['Apium', "Apium graveolens.", 0, 112],
    ['graveolens', "Apium graveolens.", 0, 112]
]
ocr_errors_with_context, nb_ocr_errors_with_context = retrieve_ocr_errors_with_context(ocr_errors)
corrected_words = retrieve_llm_corrected_words(ocr_errors_with_context, nb_ocr_errors_with_context, "mistral")
corrected_text = correct_ocr_errors_in_text(ocr_text, ocr_errors, corrected_words)
write_content_in_file("data/results/pages_concatenate/mistral_corrected_results_txt/L_école_du_jardin_potager/L_école_du_jardin_potager.txt", corrected_text, 'w')

kraken_score = generate_pairwise_score(expected_text, ocr_text)
corrected_kraken_score = generate_pairwise_score(expected_text, corrected_text)
print("kraken similarity score:", kraken_score, "out of 1.0.")
print("corrected kraken similarity score:", corrected_kraken_score, "out of 1.0.")