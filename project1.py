import csv

def csv_to_dict_list(filepath):
    with opsen(filepath, 'r', encoding = 'utf-8') as file:
        dict_reader = csv.DictReader(file)
        list_of_dicts = list(dict_reader)
    return list_of_dicts

file_path = 'data/SampleSuperstore 2.csv'
superstore_dict = csv_to_dict_list(file_path)
print(superstore_dict)
