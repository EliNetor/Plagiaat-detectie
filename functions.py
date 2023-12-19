from pathlib import Path
from spellchecker import SpellChecker
import libcst as cst

class LexiconCollector(cst.CSTTransformer):
    def __init__(self):
        self.all_words = []
    def visit_Arg(self, node):
        self.all_words.append(node.value.value)
    def visit_Name(self,node):
        self.all_words.append(node.value)

def GetComments(file_paths):
    contents = []
    for path in file_paths:
        with open(path, 'r') as f:
            lines = f.readlines()
            contents.append([line.strip() for line in lines if line.startswith('#')])
    return contents

def CheckErrors(file_paths):
    contents = []
    for path in file_paths:
        with open(path, 'r') as f:
            visitor = LexiconCollector()
            lines = f.readlines()
            source_code = ''.join(lines)
            parsed_module = cst.parse_module(source_code)
            parsed_module.visit(visitor)
            contents.append(visitor.all_words)
    
    incorrect_words = []
    for words in contents:
        spell = SpellChecker()
        misspelled = spell.unknown(words)
        incorrect_words.append(misspelled)

    d_common_errors = []
    for index, incorrect_set in enumerate(incorrect_words):
        for j, other_set in enumerate(incorrect_words):
            if index != j:
                common_errors = incorrect_set.intersection(other_set)
                if(common_errors != set()): #stop the addition of set()
                    d_common_errors.append(dict(key= index, value=[j, common_errors]))
    print(d_common_errors)
    return d_common_errors    
