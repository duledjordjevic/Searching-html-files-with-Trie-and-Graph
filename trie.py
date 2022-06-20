class TrieNode:

    def __init__(self):
        self.children = {}
        self.endOfWord = False
        self.document = {}

class Trie:

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, document, index):
        current_node = self.root

        for c in word.lower():
            if c not in current_node.children:
                current_node.children[c] = TrieNode()
            current_node = current_node.children[c]
        current_node.endOfWord = True
        if document in current_node.document.keys():
            lista = current_node.document[document]
            lista.append(index)
            current_node.document[document] = lista
        else:
            current_node.document[document] = [index]
    
    def search(self, word):
        current_node = self.root

        for c in word.lower():
            if c not in current_node.children:
                return False
            current_node = current_node.children[c]

        return current_node.endOfWord, current_node.document #Da li je bas to rec koju trazimo

    def startsWith(self, prefix):
        current_node = self.root

        for c in prefix.lower():
            if c not in current_node.children:
                return False
            current_node = current_node.children[c]

        return True


    