from pathlib import Path
from spellchecker import SpellChecker
import libcst as cst
import ast

class LexiconCollector(cst.CSTTransformer):
    def __init__(self):
        self.all_words = []
    def visit_Arg(self, node):
        self.all_words.append(node.value.value)
    def visit_Name(self,node):
        self.all_words.append(node.value)

class CSTTrans(cst.CSTTransformer):
    def leave_Comment(self, original_node, updated_node):
        return cst.RemoveFromParent()

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
    return d_common_errors    

def CheckWithoutComments(file_path1, file_path2): #methode houd geen rekening met empylines!!!!
    trees = []
    with open(file_path1, 'r') as f:
            lines = f.readlines()
            source_code = ''.join(lines)
            parsed_module = cst.parse_module(source_code)
            parsed_module = parsed_module.visit(CSTTrans())
            trees.append(parsed_module)

    with open(file_path2, 'r') as f:
            lines = f.readlines()
            source_code = ''.join(lines)
            parsed_module = cst.parse_module(source_code)
            parsed_module = parsed_module.visit(CSTTrans())
            trees.append(parsed_module)
    
    return trees[0].deep_equals(trees[1])

def CompareAst(file_path1, file_path2):
    with open(file_path1, 'r') as f1, open(file_path2, 'r') as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()
        sc1 = ''.join(lines1)
        sc2 = ''.join(lines2)
        tree1 = ast.parse(sc1)
        tree2 = ast.parse(sc2)
        
        return ast.dump(tree1) == ast.dump(tree2)