import re
from collections import defaultdict

def stack_to_string(my_stack):
    final_string = ''
    for item in my_stack:
        if item == "Bookmarks Toolbar":
            continue
        final_string += (item)
        final_string += ('-')
    return final_string

if __name__ == '__main__':
    folder_path = 'Bookmarks'
    print('Enter name of bookmark file: ')
    file_name = input()
    file_path = f'{folder_path}/{file_name}'
    print(file_path)

    #Add folder name to stack upon reading </H3>
    #Remove folder name to stack upon reading </DL><p>
    #Upon reading HREF=" add the url name to the new txt file with folder name

    folder_stack = []
    folder_dictionary = defaultdict(list)
    new_folder_string = '</H3>'
    folder_pattern = re.compile(r'<H3[^>]*>(.*?)</H3>', re.IGNORECASE)
    end_folder_pattern = re.compile(r'</DL><p>', re.IGNORECASE)
    url_pattern = re.compile(r'A HREF="(.*?)"[^>]*', re.IGNORECASE)

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            folder = folder_pattern.search(line)
            if folder:
                folder_name = folder.group(1)
                folder_name = folder_name.replace(' || ', '+')
                folder_stack.append(folder_name)
                continue
            
            if end_folder_pattern.search(line):
                folder_stack.pop()

            url = url_pattern.search(line)
            if url:
                name_list = stack_to_string(folder_stack)
                folder_dictionary[name_list].append(url.group(1))
                print(name_list + ": " + url.group(1))

    for folder, items in folder_dictionary.items():
        with open("Results/" + folder + '.txt', 'w', encoding='utf-8') as file:
            for item in items:
                file.write(item + '\n')