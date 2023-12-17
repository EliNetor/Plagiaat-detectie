from jinja2 import Environment, FileSystemLoader, select_autoescape
import webbrowser
from pathlib import Path
from collections import Counter
import os


p = Path(input("Geef een filepath op: "))

auteurs = [entry.name for entry in p.iterdir() if entry.is_dir()]
print(auteurs)

alias_mapping = {auteur: f'Auteur{i+1}' for i, auteur in enumerate(auteurs)}

opmerkingen_matrix = {alias_mapping[auteur]: {alias_mapping[andere_auteur]: [] for andere_auteur in auteurs if andere_auteur != auteur} for auteur in auteurs}

filepath = []
for auteur in auteurs:
    directory_path = p / auteur
    file_paths = directory_path.glob("*.py")
    for file_path in file_paths:
        filepath.append(file_path)

print(filepath)
counter = 0

for file_path in filepath:
    counter += 1
    selected_files = [f for f in filepath if f.name == file_path.name]
    if len(selected_files) >= 2:
        contents = {}
        for f in selected_files:
            with open(f, 'r', encoding='utf-8') as file:
                file_content = file.read()
                contents[f] = file_content
        print(contents)      
              
        same_text = [key for key, value in contents.items() if value == contents[file_path]]
        print(same_text)
        
        for item in same_text:
            if str(item) != str(file_path):
                print(file_path)
                for aut in auteurs:
                    if str(item).find(aut) > 0:
                        file_name = os.path.basename(file_path)
                        opmerkingen_matrix['Auteur' + str(counter)][alias_mapping[aut]] = [f'identieke file {file_name}']

print(opmerkingen_matrix)

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