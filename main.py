from gettext import find
from trie import Trie
from parser_ import Parser, os
from graph import Graph
from quick_sort import quick_sort
from copy import deepcopy

parser = Parser()

def find_all_dir(directory, all_dir):
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isdir(f):
            if not f.endswith("__pycache__"):
                all_dir.append(f)
            find_all_dir(f, all_dir)
    return all_dir


def find_all_htmls(directory, all_html):
    for filename in os.listdir(directory):
        f = os.path.abspath(os.path.join(directory, filename))
        # isfile = os.path.isfile(f)
        if os.path.isfile(f):
            if f.endswith(".html"):
                all_html.append(f)
        else:
            find_all_htmls(f, all_html)
def ranging(t, g, search_word, current_dir_vertexes):
    rang1 = {}
    rang2 = {}
    result = t.search(search_word)
    if result is not False:
        documents = result[1]
        if result[0]:
            for vertex in current_dir_vertexes:
                if vertex in documents.keys():
                    number_of_repetitions = len(documents[vertex])
                    number_of_incoming = g.degree(vertex, False)
                    number_of_repetitions_of_incoming = 0
                    all_incoming = g.incoming_vertexes(vertex)
                    for v in all_incoming:
                        if v in documents.keys():
                            number_of_repetitions_of_incoming += len(documents[vertex])
                    sum = int(number_of_repetitions + number_of_incoming * 0.05 + number_of_repetitions_of_incoming * 0.3)
                    rang1[sum] = vertex
                    rang2[vertex] = sum
    else:
        return None, None
    return rang1, rang2

def search_and_rang(t, g, all_html, search_word, current_dir_vertexes):
    if not g.vertex_count() > 0:
        current_dir_vertexes = []
        for html in all_html:
            lista = parser.parse(html)
            links = lista[0]
            words = lista[1]
            u = g.get_vertex(html)
            if u is None:
                u = g.insert_vertex(html)
            current_dir_vertexes.append(u)
            for link in links:
                v = g.get_vertex(link)
                if v is None:
                    v = g.insert_vertex(link)
                g.insert_edge(u, v)
            for i in range(len(words)):
                word = words[i]
                t.insert(word, u, i)
        if len(all_html) > 0:
            rang1, rang2 = ranging(t,g, search_word, current_dir_vertexes)  
            if rang1 is not None:
                return t,g, all_html, current_dir_vertexes, rang1, rang2
            else:
                return t,g, all_html, current_dir_vertexes, rang1, rang2
        else:
            current_dir_vertexes = None
            rang1 = False
            rang2 = False
            return t,g, all_html, current_dir_vertexes, rang1, rang2
    else:
        rang1, rang2 = ranging(t,g, search_word, current_dir_vertexes)  
        if rang1 is not None:
            return t,g, all_html, current_dir_vertexes, rang1, rang2
        else:
            return t,g, all_html, current_dir_vertexes, rang1, rang2
    
def ranging_for_phrase(t, g, search_words, current_dir_vertexes):
    rang1 = {}
    rang2 = {}
    documents = []
    for word in search_words:
        result = t.search(word)
        if result is not False:
            if result[0]:
                documents.append(result[1])

    if len(documents) == len(search_words):
        vertexes_with_phrase = {}
        for vertex in current_dir_vertexes:
            if vertex in documents[0].keys():
                for k,v in documents[0].items():
                    count = 0
                    lista = deepcopy(v)
                    lista2 = []
                    for dictonary in documents[1:]:
                        if k in dictonary:
                            if len(lista2) == 0:
                                for i in lista:
                                    if i+1 in dictonary[k]:
                                        lista2.append(i+1)
                                lista = []
                            else:
                                for i in lista2:
                                    if i+1 in dictonary[k]:
                                        lista.append(i+1)
                                lista2 = []
                        else:
                            lista = []
                            lista2 = []
                            break
                    if len(lista) > 0:
                        count += len(lista)
                        
                    elif len(lista2) > 0:
                        count += len(lista2)
                    
                    if count > 0:
                        vertexes_with_phrase[k] = count
        
        for vertex, value in vertexes_with_phrase.items():
            number_of_repetitions = value
             # number_of_incoming = g.degree(vertex, False)
            # number_of_repetitions_of_incoming = 0
            # all_incoming = g.incoming_vertexes(vertex)
            # for v in all_incoming:
            #     if v in vertexes_with_phrase.keys():
            #         number_of_repetitions_of_incoming += vertexes_with_phrase[v]
            
            # sum = number_of_repetitions + number_of_incoming + number_of_repetitions_of_incoming
            sum = number_of_repetitions
            rang1[sum] = vertex
            rang2[vertex] = sum

        if len(vertexes_with_phrase) == 0:
            return None, None
        else:
            return rang1, rang2
    else:
        return None, None

def search_and_rang_for_phrase(t, g, all_html, search_word, current_dir_vertexes):
    if not g.vertex_count() > 0:
        current_dir_vertexes = []
        for html in all_html:
            lista = parser.parse(html)
            links = lista[0]
            words = lista[1]
            u = g.get_vertex(html)
            if u is None:
                u = g.insert_vertex(html)
            current_dir_vertexes.append(u)
            for link in links:
                v = g.get_vertex(link)
                if v is None:
                    v = g.insert_vertex(link)
                g.insert_edge(u, v)
            for i in range(len(words)):
                word = words[i]
                t.insert(word, u, i)
        if len(all_html) > 0:
            rang1, rang2= ranging_for_phrase(t,g, search_word, current_dir_vertexes)  
            if rang1 is not None:
                return t,g, all_html, current_dir_vertexes, rang1, rang2
            else:
                return t,g, all_html, current_dir_vertexes, rang1, rang2
        else:
            current_dir_vertexes = None
            rang1 = False
            rang2 = False
            return t,g, all_html, current_dir_vertexes, rang1, rang2
    else:
        rang1, rang2 = ranging_for_phrase(t,g, search_word, current_dir_vertexes)  
        if rang1 is not None:
            return t,g, all_html, current_dir_vertexes, rang1, rang2
        else:
            return t,g, all_html, current_dir_vertexes, rang1, rang2
# t= Trie()
# g = Graph()
# all_html = []
# find_all_htmls(os.getcwd() + "\\python-2.7.7-docs-html\\faq",  all_html)
# search_and_rang(t, g, all_html, "python") 

def getList(dictonary):
    list = []
    for key in dictonary.keys():
        list.append(key)
        
    return list
def change_number_of_results(rang, sorted, number_of_result):
    while True:
        print("1.Promena broja rezultata")
        print("2.Povratak na glavni meni")
        y = input("Unesite broj koji zelite: ")
        while y != "1" and y != "2":
            print("Molim vas da unesete neki od ponudjenih brojeva!")
            y = input("Unesite broj koji zelite: ")
        if y == "1":
            m = input("Unesite broj rezultata koji zelite izlistati: ")
            while True:
                if m.isdigit():
                    m = int(m)
                    if m < 1 or m > number_of_result:
                        print("Molim vas da unesete broj u opsegu broja rezultata.")
                        m = input("Unesite broj rezultata koji zelite izlistati: ")
                    else:
                        break
                else:
                    print("Molim vas da unesete broj u opsegu broja rezultata.")
                    m = input("Unesite broj rezultata koji zelite izlistati: ")
            m = int(m)
            print("\nRezultati pretrage:\n")
            for i in range(1, m+1):
                print("\t" + str(rang[sorted[-i]]).split('\\')[-1] + " : " + str(sorted[-i]))
            print("")
        else:
            break

def searching_AND(x, t, g, all_html, current_dir_vertexes):
    if x.index("AND") == 1:
        t, g, all_html, current_dir_vertexes, rang1, rang2 = search_and_rang(t, g, all_html, x[0], current_dir_vertexes)
        t, g, all_html, current_dir_vertexes, rang3, rang4 = search_and_rang(t, g, all_html, x[2], current_dir_vertexes)
        if (rang1 is not None and rang1) and (rang3 is not None and rang3):
            rang_intersection = {}
            for k,v in rang2.items():
                if k in rang4:
                    rang_intersection[k] = rang2[k] + rang2[k]
                    
            rang = {v:k for k,v in rang_intersection.items()}
                
            if len(rang) != 0:
                sorted = getList(rang)
                sorted = quick_sort(sorted)
                number_of_result = len(sorted)
                print("Broj rezultata: " + str(number_of_result))
                print("\nRezultati pretrage:\n")
                if number_of_result > 10:
                    document = t.search(x[0])[1]
                    indexes = document[rang[sorted[-1]]]
                    words = parser.parse(str(rang[sorted[-1]]))[1]
                    try:
                        print("\t" + str(rang[sorted[-1]]).split('\\')[-1] + " : " + str(sorted[-1]))
                        print("\033[1m" +"\t\t" + words[indexes[0]] + " " + words[indexes[0] + 1] + " " + words[indexes[0] + 2] + "...")
                    except:
                        print("\t" + str(rang[sorted[-1]]).split('\\')[-1] + " : " + str(sorted[-1]))
                    for i in range(2, 11):
                        print("\033[0m" + "\t" + str(rang[sorted[-i]]).split('\\')[-1] + " : " + str(sorted[-i]))
                    print("")
                else:
                    document = t.search(x[0])[1]
                    indexes = document[rang[sorted[-1]]]
                    words = parser.parse(str(rang[sorted[-1]]))[1]
                    try:
                        print("\t" + str(rang[sorted[-1]]).split('\\')[-1] + " : " + str(sorted[-1]))
                        print("\033[1m" +"\t\t" + words[indexes[0]] + " " + words[indexes[0] + 1] + " " + words[indexes[0] + 2] + "...")
                    except:
                        print("\t" + str(rang[sorted[-1]]).split('\\')[-1] + " : " + str(sorted[-1]))
                    for i in range(2, number_of_result + 1):
                        print("\033[0m" + "\t" + str(rang[sorted[-i]]).split('\\')[-1] + " : " + str(sorted[-i]))
                    print("")
                
                change_number_of_results(rang, sorted, number_of_result) 
            else:
                print("Nismo pronasli obe reci ni u jednom dokumentu.")
            
        elif rang1 is None or rang3 is None:
            print("Nismo pronasli ove reci. Pokusajte ponovo")
        else:
            print("Nazalost u ovom fajlu nema html fajlova i ne mozete pretraziti nista")
    else:
        print("Molim vas da pravilo unesete pretragu.")

    return t, g, all_html, current_dir_vertexes

def searching_OR(x, t, g, all_html, current_dir_vertexes):
    if x.index("OR") == 1:
        find_words = {}
        t, g, all_html, current_dir_vertexes, rang1, rang2 = search_and_rang(t, g, all_html, x[0], current_dir_vertexes)
        t, g, all_html, current_dir_vertexes, rang3, rang4 = search_and_rang(t, g, all_html, x[2], current_dir_vertexes)
        if (rang1 is not None and rang1) or (rang3 is not None and rang3):
            if rang1 is None or rang1 is False:
                rang = rang3
                for k,v in rang4.items():
                    if k not in find_words:
                        find_words[k] = x[2]
            elif rang3 is None or rang3 is False:
                rang = rang1
                for k,v in rang2.items():
                    if k not in find_words:
                        find_words[k] = x[0]
            else:
                rang_union = {**rang2, **rang4}
                # for k,v in rang_union.items():
                #     if k not in find_words:
                #         find_words[k] = x[0]
                rang_union_2 = {}
                for k,v in rang_union.items():
                    if k in rang2 and k in rang4:
                        rang_union_2[k] = rang2[k] + rang2[k]
                        find_words[k] = x[0]
                    else:
                        if k in rang2:
                            rang_union_2[k] = rang2[k]
                            find_words[k] = x[0]
                        else:
                            rang_union_2[k] = rang4[k]
                            find_words[k] = x[2]
                rang = {v:k for k,v in rang_union_2.items()}
                
            if len(rang) != 0:
                sorted = getList(rang)
                sorted = quick_sort(sorted)
                number_of_result = len(sorted)
                print("Broj rezultata: " + str(number_of_result))
                print("\nRezultati pretrage:\n")
                if number_of_result > 10:
                    document = t.search(find_words[rang[sorted[-1]]])[1]
                    indexes = document[rang[sorted[-1]]]
                    words = parser.parse(str(rang[sorted[-1]]))[1]
                    try:
                        print("\t" + str(rang[sorted[-1]]).split('\\')[-1] + " : " + str(sorted[-1]))
                        print("\033[1m" +"\t\t" + words[indexes[0]] + " " + words[indexes[0] + 1] + " " + words[indexes[0] + 2] + "...")
                    except:
                        print("\t" + str(rang[sorted[-1]]).split('\\')[-1] + " : " + str(sorted[-1]))
                    for i in range(2, 11):
                        print("\033[0m" + "\t" + str(rang[sorted[-i]]).split('\\')[-1] + " : " + str(sorted[-i]))
                    print("")
                else:
                    document = t.search(find_words[rang[sorted[-1]]])[1]
                    indexes = document[rang[sorted[-1]]]
                    words = parser.parse(str(rang[sorted[-1]]))[1]
                    try:
                        print("\t" + str(rang[sorted[-1]]).split('\\')[-1] + " : " + str(sorted[-1]))
                        print("\033[1m" +"\t\t" + words[indexes[0]] + " " + words[indexes[0] + 1] + " " + words[indexes[0] + 2] + "...")
                    except:
                        print("\t" + str(rang[sorted[-1]]).split('\\')[-1] + " : " + str(sorted[-1]))
                    for i in range(2, number_of_result + 1):
                        print("\033[0m" + "\t" + str(rang[sorted[-i]]).split('\\')[-1] + " : " + str(sorted[-i]))
                    print("")
                
                change_number_of_results(rang, sorted, number_of_result) 
            else:
                print("Nismo pronasli ni jednu od ovih reci.")
            
        elif rang1 is None and rang2 is None:
            print("Nismo pronasli ovu rec. Pokusajte ponovo")
        else:
            print("Nazalost u ovom fajlu nema html fajlova i ne mozete pretraziti nista")
    else:
        print("Molim vas da pravilo unesete pretragu.")

    return t, g, all_html, current_dir_vertexes

def searching_NOT(x, t, g, all_html, current_dir_vertexes):
    if x.index("NOT") == 1:
        t, g, all_html, current_dir_vertexes, rang1, rang2 = search_and_rang(t, g, all_html, x[0], current_dir_vertexes)
        t, g, all_html, current_dir_vertexes, rang3, rang4 = search_and_rang(t, g, all_html, x[2], current_dir_vertexes)
        if (rang1 is not None and rang1):
            if rang3 is None or rang3 is False:
                rang = rang1
            else:
                rang_difference = {k:v for k,v in rang2.items() if k not in rang4}
                rang = {v:k for k,v in rang_difference.items()}

            if len(rang) != 0:
                sorted = getList(rang)
                sorted = quick_sort(sorted)
                number_of_result = len(sorted)
                print("Broj rezultata: " + str(number_of_result))
                print("\nRezultati pretrage:\n")
                if number_of_result > 10:
                    document = t.search(x[0])[1]
                    indexes = document[rang[sorted[-1]]]
                    words = parser.parse(str(rang[sorted[-1]]))[1]
                    try:
                        print("\t" + str(rang[sorted[-1]]).split('\\')[-1] + " : " + str(sorted[-1]))
                        print("\033[1m" +"\t\t" + words[indexes[0]] + " " + words[indexes[0] + 1] + " " + words[indexes[0] + 2] + "...")
                    except:
                        print("\t" + str(rang[sorted[-1]]).split('\\')[-1] + " : " + str(sorted[-1]))
                    for i in range(2, 11):
                        print("\033[0m" + "\t" + str(rang[sorted[-i]]).split('\\')[-1] + " : " + str(sorted[-i]))
                    print("")
                else:
                    document = t.search(x[0])[1]
                    indexes = document[rang[sorted[-1]]]
                    words = parser.parse(str(rang[sorted[-1]]))[1]
                    try:
                        print("\t" + str(rang[sorted[-1]]).split('\\')[-1] + " : " + str(sorted[-1]))
                        print("\033[1m" +"\t\t" + words[indexes[0]] + " " + words[indexes[0] + 1] + " " + words[indexes[0] + 2] + "...")
                    except:
                        print("\t" + str(rang[sorted[-1]]).split('\\')[-1] + " : " + str(sorted[-1]))
                    for i in range(2, number_of_result + 1):
                        print("\033[0m" + "\t" + str(rang[sorted[-i]]).split('\\')[-1] + " : " + str(sorted[-i]))
                    print("")
                
                change_number_of_results(rang, sorted, number_of_result) 
            else:
                print("Nismo pronasli ovakav zahtev")
            
        elif rang1 is None:
            print("Nismo pronasli prvu rec. Pokusajte ponovo")
        else:
            print("Nazalost u ovom fajlu nema html fajlova i ne mozete pretraziti nista")
    else:
        print("Molim vas da pravilo unesete pretragu.")

    return t, g, all_html, current_dir_vertexes

def searching_multiword(x, t, g, all_html, current_dir_vertexes):
    rang_union = {}
    tf = False
    find_words = {}
    for i in range(len(x)):
        t, g, all_html, current_dir_vertexes, rang1, rang2 = search_and_rang(t, g, all_html, x[i], current_dir_vertexes)
        if rang1 is not None and rang1:
            for k,v in rang2.items():
                if k not in find_words:
                    find_words[k] = x[i]
                if k in rang_union:
                    rang_union[k] = v + rang_union[k]
                else:
                    rang_union[k] = v

        if rang1 is False:
            tf = not tf
    rang = {v:k for k,v in rang_union.items()}
    if len(rang) != 0:
        sorted = getList(rang)
        sorted = quick_sort(sorted)
        number_of_result = len(sorted)
        print("Broj rezultata: " + str(number_of_result))
        print("\nRezultati pretrage:\n")
        if number_of_result > 10:
            document = t.search(find_words[rang[sorted[-1]]])[1]
            indexes = document[rang[sorted[-1]]]
            words = parser.parse(str(rang[sorted[-1]]))[1]
            try:
                print("\t" + str(rang[sorted[-1]]).split('\\')[-1] + " : " + str(sorted[-1]))
                print("\033[1m" +"\t\t" + words[indexes[0]] + " " + words[indexes[0] + 1] + " " + words[indexes[0] + 2] + "...")
            except:
                print("\t" + str(rang[sorted[-1]]).split('\\')[-1] + " : " + str(sorted[-1]))
            for i in range(2, 11):
                print("\033[0m" + "\t" + str(rang[sorted[-i]]).split('\\')[-1] + " : " + str(sorted[-i]))
            print("")
        else:
            document = t.search(find_words[rang[sorted[-1]]])[1]
            indexes = document[rang[sorted[-1]]]
            words = parser.parse(str(rang[sorted[-1]]))[1]
            try:
                print("\t" + str(rang[sorted[-1]]).split('\\')[-1] + " : " + str(sorted[-1]))
                print("\033[1m" +"\t\t" + words[indexes[0]] + " " + words[indexes[0] + 1] + " " + words[indexes[0] + 2] + "...")
            except:
                print("\t" + str(rang[sorted[-1]]).split('\\')[-1] + " : " + str(sorted[-1]))
            for i in range(2, number_of_result + 1):
                print("\033[0m" + "\t" + str(rang[sorted[-i]]).split('\\')[-1] + " : " + str(sorted[-i]))
            print("")
        
        change_number_of_results(rang, sorted, number_of_result) 
    else:
        if tf:
            print("Nazalost u ovom fajlu nema html fajlova i ne mozete pretraziti nista")
        else:
            print("Nismo pronasli ni jednu od ovih reci.")
    return t, g, all_html, current_dir_vertexes

def searching_phrase(x, t, g, all_html, current_dir_vertexes):
    t, g, all_html, current_dir_vertexes, rang1, rang2 = search_and_rang_for_phrase(t, g, all_html, x, current_dir_vertexes)
    if rang1 is not None and rang1:
        sorted = getList(rang1)
        sorted = quick_sort(sorted)
        number_of_result = len(sorted)
        print("Broj rezultata: " + str(number_of_result))
        print("\nRezultati pretrage:\n")
        if number_of_result > 10:
            document = t.search(x[0])[1]
            indexes = document[rang1[sorted[-1]]]
            words = parser.parse(str(rang1[sorted[-1]]))[1]
            index_of_first = None
            for index in indexes:
                for y in range(len(x[1:])):
                    if x[1:][y].lower() == words[index + y + 1].lower():
                        if y == len(x[1:]) - 1:
                            index_of_first = index
                            break
            try:
                print("\t" + str(rang1[sorted[-1]]).split('\\')[-1] + " : " + str(sorted[-1]))
                print("\033[1m" +"\t\t" + words[index_of_first] + " " + words[index_of_first + 1] + " " + words[index_of_first + 2]  + " " + words[index_of_first + 3] +  " " + words[index_of_first + 4] + "...")
            except:
                print("\t" + str(rang1[sorted[-1]]).split('\\')[-1] + " : " + str(sorted[-1]))
            for i in range(2, 11):
                print("\033[0m" + "\t" + str(rang1[sorted[-i]]).split('\\')[-1] + " : " + str(sorted[-i]))
            print("")

        else:
            document = t.search(x[0])[1]
            indexes = document[rang1[sorted[-1]]]
            words = parser.parse(str(rang1[sorted[-1]]))[1]
            index_of_first = None
            for index in indexes:
                for y in range(len(x[1:])):
                    if x[1:][y].lower() == words[index + y + 1].lower():
                        if y == len(x[1:]) - 1:
                            index_of_first = index
                            break
            try:
                print("\t" + str(rang1[sorted[-1]]).split('\\')[-1] + " : " + str(sorted[-1]))
                print("\033[1m" +"\t\t" + words[index_of_first] + " " + words[index_of_first + 1] + " " + words[index_of_first + 2]  + " " + words[index_of_first + 3] +  " " + words[index_of_first + 4] + "...")
            except:
                print("\t" + str(rang1[sorted[-1]]).split('\\')[-1] + " : " + str(sorted[-1]))
            for i in range(2, number_of_result + 1):
                print("\033[0m" + "\t" + str(rang1[sorted[-i]]).split('\\')[-1] + " : " + str(sorted[-i]))
            print("")
        
        change_number_of_results(rang1, sorted, number_of_result) 
        
    elif rang1 is None:
        print("Nismo pronasli ovu rec. Pokusajte ponovo")
    else:
        print("Nazalost u ovom fajlu nema html fajlova i ne mozete pretraziti nista")
    
    return t, g, all_html, current_dir_vertexes

def search_one_word(x, t, g, all_html, current_dir_vertexes):
    x = x[0]
    if x[0] == '"' and x[-1] == '"':
        x = x.replace('"', "")
    t, g, all_html, current_dir_vertexes, rang1, rang2 = search_and_rang(t, g, all_html, x, current_dir_vertexes)
    if rang1 is not None and rang1:
        sorted = getList(rang1)
        sorted = quick_sort(sorted)
        number_of_result = len(sorted)
        print("Broj rezultata: " + str(number_of_result))
        print("\nRezultati pretrage:\n")
        if number_of_result > 10:
            document = t.search(x)[1]
            indexes = document[rang1[sorted[-1]]]
            words = parser.parse(str(rang1[sorted[-1]]))[1]
            try:
                print("\t" + str(rang1[sorted[-1]]).split('\\')[-1] + " : " + str(sorted[-1]))
                print("\033[1m" +"\t\t" + words[indexes[0]] + " " + words[indexes[0] + 1] + " " + words[indexes[0] + 2] + "...")
            except:
                print("\t" + str(rang1[sorted[-1]]).split('\\')[-1] + " : " + str(sorted[-1]))
            for i in range(2, 11):
                print("\033[0m" + "\t" + str(rang1[sorted[-i]]).split('\\')[-1] + " : " + str(sorted[-i]))
            print("")
        else:
            document = t.search(x)[1]
            indexes = document[rang1[sorted[-1]]]
            words = parser.parse(str(rang1[sorted[-1]]))[1]
            try:
                print("\t" + str(rang1[sorted[-1]]).split('\\')[-1] + " : " + str(sorted[-1]))
                print("\033[1m" +"\t\t" + words[indexes[0]] + " " + words[indexes[0] + 1] + " " + words[indexes[0] + 2] + "...")
            except:
                print("\t" + str(rang1[sorted[-1]]).split('\\')[-1] + " : " + str(sorted[-1]))
            for i in range(2, number_of_result + 1):
                print("\033[0m" + "\t" + str(rang1[sorted[-i]]).split('\\')[-1] + " : " + str(sorted[-i]))
            print("")
        
        change_number_of_results(rang1, sorted, number_of_result) 
        
    elif rang1 is None:
        print("Nismo pronasli ovu rec. Pokusajte ponovo")
    else:
        print("Nazalost u ovom fajlu nema html fajlova i ne mozete pretraziti nista")
    
    return t, g, all_html, current_dir_vertexes

def searching():
    default_directory = os.getcwd() + "\\python-2.7.7-docs-html"
    directory = os.getcwd() + "\\python-2.7.7-docs-html"
    last_search_dir = None
    t = Trie()
    g = Graph()
    current_dir_vertexes = None
    rang1, rang2 = None, None
    all_html = []
    while True:
        print("Folder u kome se trenutno nalazite: " + directory)
        print("1.Promenite direktorijum")
        print("2.Pretrazite rec")
        if directory != os.getcwd() + "\\python-2.7.7-docs-html":
            print("3.Vratite se na pocetni direktorijum")
            print("4.Izlaz")
            y = input("Unesite broj koji zelite: ")
            while y != "1" and y != "2" and y != "3" and y != "4":
                print("Molim vas da unesete neki od ponudjenih brojeva!")
                y = input("Unesite broj koji zelite: ")
        else:
            print("3.Izlaz")
            y = input("Unesite broj koji zelite: ")
            while y != "1" and y != "2" and y != "3":
                print("Molim vas da unesete neki od ponudjenih brojeva!")
                y = input("Unesite broj koji zelite: ")
        y = int(y)
        if y == 1:
            x = input("Unesite apsolutnu putanju direktorijuma koji zelite da pretrazite: ")
            all_dir = []
            all_dir = find_all_dir(default_directory, all_dir)

            while x not in all_dir:
                print("Unesite pravilno putanju.")
                x = input("Unesite punu putanju do direktorijuma koji zelite da pretrazite: ")
            directory = x

        elif y == 2:
            x = input("Search: ")
            while x == "":
                print("Morate uneti rec!")
                x = input("Search: ")
            if last_search_dir != directory:
                last_search_dir = directory
                all_html = []
                find_all_htmls(directory, all_html)
                t = Trie()
                g = Graph()
                current_dir_vertexes = None
                x = x.split()
                if len(x) == 1:
                    t, g, all_html, current_dir_vertexes = search_one_word(x, t, g, all_html, current_dir_vertexes)
                else:
                    if x[0][0] == '"' and x[-1][-1] == '"':
                        x[0] = x[0].replace('"', "")
                        x[-1] = x[-1].replace('"', "")
                        
                        t, g, all_html, current_dir_vertexes = searching_phrase(x, t, g, all_html, current_dir_vertexes)
                    else:
                        if len(x) == 3 and ("AND" in x or "OR" in x or "NOT" in x):
                            if "AND" in x:
                                t, g, all_html, current_dir_vertexes = searching_AND(x, t, g, all_html, current_dir_vertexes)
                            elif "OR" in x:
                                t, g, all_html, current_dir_vertexes = searching_OR(x, t, g, all_html, current_dir_vertexes)
                            elif "NOT" in x:
                                t, g, all_html, current_dir_vertexes = searching_NOT(x, t, g, all_html, current_dir_vertexes)
                        else:
                            t, g, all_html, current_dir_vertexes = searching_multiword(x, t, g, all_html, current_dir_vertexes)

            else:
                x = x.split()
                if len(x) == 1:
                    t, g, all_html, current_dir_vertexes = search_one_word(x, t, g, all_html, current_dir_vertexes)
                else:
                    if x[0][0] == '"' and x[-1][-1] == '"':
                        x[0] = x[0].replace('"', "")
                        x[-1] = x[-1].replace('"', "")
                        
                        t, g, all_html, current_dir_vertexes = searching_phrase(x, t, g, all_html, current_dir_vertexes)
                    else:
                        if len(x) == 3 and ("AND" in x or "OR" in x or "NOT" in x):
                            if "AND" in x:
                                t, g, all_html, current_dir_vertexes = searching_AND(x, t, g, all_html, current_dir_vertexes)
                            elif "OR" in x:
                                t, g, all_html, current_dir_vertexes = searching_OR(x, t, g, all_html, current_dir_vertexes)
                            elif "NOT" in x:
                                t, g, all_html, current_dir_vertexes = searching_NOT(x, t, g, all_html, current_dir_vertexes)
                        else:
                            t, g, all_html, current_dir_vertexes = searching_multiword(x, t, g, all_html, current_dir_vertexes)

        else:
            if y == 3:
                if directory != os.getcwd() + "\\python-2.7.7-docs-html":
                    directory = os.getcwd() + "\\python-2.7.7-docs-html"
                else:
                    break
            else:
                break
            

if __name__ == '__main__':
    searching()
