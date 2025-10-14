import csv

def csv_to_dict_list(filepath):
    with open(filepath, 'r', encoding = 'utf-8') as file:
        dict_reader = csv.DictReader(file)
        list_of_dicts = list(dict_reader)
    return list_of_dicts

def clean_data(superstore_dict):
    for data in superstore_dict: 
        for k,v in data.items():
            if isinstance(v,str):
                v.strip()
            if k =='Sales':
                data['Sales']=float(v)
            if k=='Profit':
                data['Profit']=float(v)
    return superstore_dict

if __name__ == "__main__":
    file_path = 'data/SampleSuperstore 2.csv'
    superstore_dict = csv_to_dict_list(file_path)
    superstore_data = clean_data(superstore_dict)
    print(superstore_data)
