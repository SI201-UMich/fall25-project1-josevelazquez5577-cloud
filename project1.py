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

def calc_region_profit(superstore_data):
    profit_list = [
        {'Region': 'Central', 'Total Sales': 0.0, 'Total Profit': 0.0, 'Profit Margin': 0.0}, 
        {'Region': 'East', 'Total Sales': 0.0, 'Total Profit': 0.0, 'Profit Margin': 0.0},
        {'Region': 'South', 'Total Sales': 0.0, 'Total Profit': 0.0, 'Profit Margin': 0.0},
        {'Region': 'West', 'Total Sales': 0.0, 'Total Profit': 0.0, 'Profit Margin': 0.0}       
    ]
    for row in superstore_data:
        if row['Region'] == 'Central':
            profit_list[0]['Total Sales'] += row['Sales']
            profit_list[0]['Total Profit'] += row['Profit']
        elif row['Region'] == 'East':
            profit_list[1]['Total Sales'] += row['Sales']
            profit_list[1]['Total Profit'] += row['Profit']
        elif row['Region'] == 'South':
            profit_list[2]['Total Sales'] += row['Sales']
            profit_list[2]['Total Profit'] += row['Profit']
        elif row['Region'] == 'West':
            profit_list[3]['Total Sales'] += row['Sales']
            profit_list[3]['Total Profit'] += row['Profit']
    profit_list[0]['Profit Margin'] = profit_list[0]['Total Profit']/profit_list[0]['Total Sales']*100
    profit_list[1]['Profit Margin'] = profit_list[1]['Total Profit']/profit_list[1]['Total Sales']*100
    profit_list[2]['Profit Margin'] = profit_list[2]['Total Profit']/profit_list[2]['Total Sales']*100
    profit_list[3]['Profit Margin'] = profit_list[3]['Total Profit']/profit_list[3]['Total Sales']*100
    fieldnames = ['Region','Total Sales','Total Profit','Profit Margin']
    result_file = 'data/result1.csv'
    list_to_csv(profit_list, result_file, fieldnames)


if __name__ == "__main__":
    file_path = 'data/SampleSuperstore 2.csv'
    superstore_dict = csv_to_dict_list(file_path)
    superstore_data = clean_data(superstore_dict)
    print(superstore_data)
