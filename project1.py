from collections import defaultdict
import csv
from operator import itemgetter

def load_csv(filepath):
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

def calc_region_profitability(superstore_data):
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
    result_file = 'result/result1.csv'
    write_csv(profit_list, result_file, fieldnames)

def calc_top_subcats_by_region(superstore_data):
    sorted_average_sales = get_average_sales(superstore_data)
    sorted_top_average_sales = get_top_average_sales(sorted_average_sales, k = 5)
    fieldnames = ['Region', 'Sub-Category', 'Average Sales']
    result_file = 'result/result2.csv'
    write_csv(sorted_top_average_sales, result_file, fieldnames)

def get_average_sales(superstore_data):
    group_data = defaultdict(lambda: {'Total Sales': 0, 'Count': 0})

    for row in superstore_data:
        key = (row['Region'], row['Sub-Category'])
        group_data[key]['Total Sales'] += row['Sales']
        group_data[key]['Count'] += 1

    average_sales = []
    for (region, subcategory), values in group_data.items():
        average = values['Total Sales']/values['Count']
        average_sales.append({'Region': region, 'Sub-Category': subcategory, 'Average Sales': average})
    
    sorted_average_sales = sorted(average_sales, key = itemgetter('Region', 'Average Sales'), reverse = True)
    return sorted_average_sales

def get_top_average_sales(sorted_average_sales, k = 5):
    top_average_sales = []
    count_south = 0
    count_east = 0
    count_west = 0
    count_central = 0
    for row in sorted_average_sales:
        if row['Region'] == 'South' and count_south < k:
            count_south += 1
            top_average_sales.append(row)
        elif row['Region'] == 'East' and count_east < k:
            count_east += 1
            top_average_sales.append(row)
        elif row['Region'] == 'West' and count_west < k:
            count_west += 1
            top_average_sales.append(row)
        elif row['Region'] == 'Central' and count_central < k:
            count_central += 1
            top_average_sales.append(row)
    sorted_top_average_sales = sorted(top_average_sales, key = itemgetter('Region', 'Average Sales'), reverse = True)
    return sorted_top_average_sales



def write_csv(dict_list, result_file, fieldnames):
    with open(result_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(dict_list)

if __name__ == "__main__":
    file_path = 'data/SampleSuperstore 2.csv'
    superstore_dict = load_csv(file_path)
    superstore_data = clean_data(superstore_dict)
    calc_region_profitability(superstore_data)
    calc_top_subcats_by_region(superstore_data)
    print(superstore_data)
