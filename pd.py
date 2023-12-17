from jinja2 import Environment, FileSystemLoader, select_autoescape
import webbrowser

auteurs = ['Vincent', 'Lisa', 'David']

alias_mapping = {auteur: f'Auteur{i+1}' for i, auteur in enumerate(auteurs)}

opmerkingen_matrix = {alias_mapping[auteur]: {alias_mapping[andere_auteur]: [] for andere_auteur in auteurs if andere_auteur != auteur} for auteur in auteurs}

opmerkingen_matrix['Auteur1']['Auteur2'] = ['test']
opmerkingen_matrix['Auteur2']['Auteur3'] = ['test2']
opmerkingen_matrix['Auteur3']['Auteur3'] = ['test3']

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