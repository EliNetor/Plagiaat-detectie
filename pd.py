from jinja2 import Environment, FileSystemLoader, select_autoescape
import webbrowser
from pathlib import Path
import os
import functions


p = Path(input("Geef een filepath op: "))

auteurs = [entry.name for entry in p.iterdir() if entry.is_dir()]

alias_mapping = {auteur: f'Auteur{i+1}' for i, auteur in enumerate(auteurs)}

opmerkingen_matrix = {alias_mapping[auteur]: {alias_mapping[andere_auteur]: [] for andere_auteur in auteurs if andere_auteur != auteur} for auteur in auteurs}

for aut in auteurs:
    filepath_aut = []
    filepath_aut2 = []

    directory_path = p / aut
    file_paths2 = directory_path.glob("*.py")
    for file_path in file_paths2:
        filepath_aut.append(file_path)

    for aut2 in auteurs:
        if aut != aut2:
            filepath_aut2 = []
            directory_path = p / aut2
            file_paths2 = directory_path.glob("*.py")
            for file_path in file_paths2:
                 filepath_aut2.append(file_path)
            
            #checks for same filename and content
            for file_path in filepath_aut:
                selected_files = [f for f in filepath_aut2 if f.name == file_path.name]
                if len(selected_files) >= 1:
                    contents = {}
                    for f in selected_files:
                        with open(f, 'r', encoding='utf-8') as file:
                            file_content = file.read()
                            contents[f] = file_content     
  
                    same_text = [key for key, value in contents.items() if value == contents[selected_files[0]]]
                    
                    for item in same_text:
                        if str(item) != str(file_path):
                                file_name = os.path.basename(file_path)
                                opmerkingen_matrix[alias_mapping[aut]][alias_mapping[aut2]] = [f'identieke file {file_name}']


            #checks for comment lines
            comment_lines1 = functions.GetComments(filepath_aut)
            comment_lines2 = functions.GetComments(filepath_aut2)
            counter = 0
            for lines1 in comment_lines1:
                for lines2 in comment_lines2:
        
                    common_lines = set(lines1) & set(lines2)

                    if common_lines:
                        counter += 1
                        if not opmerkingen_matrix[alias_mapping[aut]][alias_mapping[aut2]]:
                            opmerkingen_matrix[alias_mapping[aut]][alias_mapping[aut2]] += [f"Common lines: {common_lines}"]
                            opmerkingen_matrix[alias_mapping[aut2]][alias_mapping[aut]] += [f"Common lines: {common_lines}"]
                        break
            
            #check for commons spelling mistakes
            d_mistakes = functions.CheckErrors(filepath_aut + filepath_aut2)
            for entry in d_mistakes:
                new_entry = f"The similar mistakes are: {entry['value'][1]}"
                if new_entry not in opmerkingen_matrix[alias_mapping[aut]][alias_mapping[aut2]]:
                    opmerkingen_matrix[alias_mapping[aut]][alias_mapping[aut2]].append(new_entry)

            #check if file is the same without comment lines
            if len(filepath_aut) == len(filepath_aut2):
                for f1 in filepath_aut:
                    for f2 in filepath_aut2:
                        if functions.CheckWithoutComments(f1, f2):
                            new_entry = f"2 or more files are identical without comments"
                            if new_entry not in opmerkingen_matrix[alias_mapping[aut]][alias_mapping[aut2]]:
                                opmerkingen_matrix[alias_mapping[aut]][alias_mapping[aut2]].append(new_entry)
                            if new_entry not in opmerkingen_matrix[alias_mapping[aut2]][alias_mapping[aut]]:
                                opmerkingen_matrix[alias_mapping[aut2]][alias_mapping[aut]].append(new_entry) 

            #check if file is the same with ast
            for f1 in filepath_aut:
                for f2 in filepath_aut2:
                    if functions.CompareAst(f1,f2):
                        new_entry = f"{f1.name} and {f2.name} are identical acording to AST"
                        if new_entry not in opmerkingen_matrix[alias_mapping[aut]][alias_mapping[aut2]]:
                            opmerkingen_matrix[alias_mapping[aut]][alias_mapping[aut2]].append(new_entry)

env = Environment(
    loader=FileSystemLoader("."),
    autoescape=select_autoescape()
)
template = env.get_template('./templates/template.html')
output = template.render(opmerkingen_matrix=opmerkingen_matrix, auteurs=alias_mapping.values())

file_name = input("Hoe moet de html file genoemd worden? ")

with open(file_name, 'w', encoding='utf-8') as file:
    file.write(output)

webbrowser.open(file_name)