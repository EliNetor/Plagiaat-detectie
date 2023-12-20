from jinja2 import Environment, FileSystemLoader, select_autoescape
import webbrowser
from pathlib import Path
import os
import functions


p = Path(input("Geef een filepath op: "))

auteurs = [entry.name for entry in p.iterdir() if entry.is_dir()]

alias_mapping = {auteur: f'Auteur{i+1}' for i, auteur in enumerate(auteurs)}

opmerkingen_matrix = {alias_mapping[auteur]: {alias_mapping[andere_auteur]: [] for andere_auteur in auteurs if andere_auteur != auteur} for auteur in auteurs}

#creates the filepath for every autor in the directory
filepath = []
for auteur in auteurs:
    directory_path = p / auteur
    file_paths = directory_path.glob("*.py")
    for file_path in file_paths:
        filepath.append(file_path)

counter = 0

#checks for same filename and content
for file_path in filepath:
    counter += 1
    selected_files = [f for f in filepath if f.name == file_path.name]
    if len(selected_files) >= 2:
        contents = {}
        for f in selected_files:
            with open(f, 'r', encoding='utf-8') as file:
                file_content = file.read()
                contents[f] = file_content     
              
        same_text = [key for key, value in contents.items() if value == contents[file_path]]
        print(same_text)
        
        for item in same_text:
            if str(item) != str(file_path):
                for aut in auteurs:
                    if str(item).find(aut) > 0:
                        file_name = os.path.basename(file_path)
                        opmerkingen_matrix['Auteur' + str(counter)][alias_mapping[aut]] = [f'identieke file {file_name}']


#checks for comment lines
comment_lines = functions.GetComments(filepath)
counter = 0
for i, lines1 in enumerate(comment_lines):
    for j, lines2 in enumerate(comment_lines):
        if i != j: 
            common_lines = set(lines1) & set(lines2)
            if common_lines:
                counter += 1
                if not opmerkingen_matrix['Auteur' + str(i+1)]['Auteur' + str(j+1)]:
                    opmerkingen_matrix['Auteur' + str(i+1)]['Auteur' + str(j+1)] = [f"Common lines: {common_lines}"]
                    opmerkingen_matrix['Auteur' + str(j+1)]['Auteur' + str(i+1)] = [f"Common lines: {common_lines}"]
                break

#check for commons spelling mistakes
d_mistakes = functions.CheckErrors(filepath)
print(d_mistakes)
for entry in d_mistakes:
    opmerkingen_matrix["Auteur" + str(entry['key'] + 1)]["Auteur" + str(entry['value'][0] + 1)] += [f"The similar mistakes are: {entry['value'][1]}"]

#check if file is the same without comment lines
for i, p in enumerate(filepath):
    for j, p2 in enumerate(filepath):
        if i != j:
            if functions.CheckWithoutComments(filepath[i], filepath[j]):
                 opmerkingen_matrix["Auteur" + str(i + 1)]["Auteur" + str(j + 1)] += [f"Files are identical without comments"]

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