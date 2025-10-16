# Name: Jose Velazquez
# Student ID: 86871146
# Email: josevel@umich.edu
# Collaborators: None
# GenAI Usage: helped me with test cases and grouping data.
# Function Authorship: All functions written by Jose Velazquez

from collections import defaultdict
import csv
from operator import itemgetter


def load_csv(filepath):
    """Reads a CSV file and transforms it into a list of dictionaries."""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            dict_reader = csv.DictReader(file)
            list_of_dicts = list(dict_reader)
        return list_of_dicts
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
        return [] # Return an empty list to prevent crashes

def clean_data(superstore_list):
    """
    Cleans and validates data - removes whitespace, and converts numeric
    fields from string to float.
    """
    if not superstore_list:
        return []
        
    for row in superstore_list:
        # Clean whitespace from all string values
        for key, value in row.items():
            if isinstance(value, str):
                row[key] = value.strip()
        
        # Convert Sales and Profit to float, handle potential errors
        try:
            row['Sales'] = float(row.get('Sales', 0.0))
            row['Profit'] = float(row.get('Profit', 0.0))
        except (ValueError, TypeError):
            # If conversion fails, set to 0.0
            row['Sales'] = 0.0
            row['Profit'] = 0.0
            
    return superstore_list


def calc_region_profitability(superstore_data):
    """
    Groups data by region and calculates total sales, total profit, and profit margin.
    Returns a list of dictionaries with the results.
    """
    # Using a dictionary is more flexible than a hardcoded list
    region_summary = defaultdict(lambda: {'Total Sales': 0.0, 'Total Profit': 0.0})

    for row in superstore_data:
        region = row.get('Region')
        if region: # Only process rows that have a region
            region_summary[region]['Total Sales'] += row.get('Sales', 0.0)
            region_summary[region]['Total Profit'] += row.get('Profit', 0.0)
    
    # Now, format the results into the desired list of dictionaries
    profit_list = []
    for region, data in region_summary.items():
        margin = 0.0
        # CRITICAL: Check for zero sales to prevent division errors
        if data['Total Sales'] != 0:
            margin = (data['Total Profit'] / data['Total Sales']) * 100
        
        profit_list.append({
            'Region': region,
            'Total Sales': data['Total Sales'],
            'Total Profit': data['Total Profit'],
            'Profit Margin': margin
        })
        
    return profit_list 

def calc_top_subcats_by_region(superstore_data, k=5):
    """
    Finds the top k subcategories by average sales for each region.
    Returns a sorted list of dictionaries with the results.
    """
    sorted_average_sales = get_average_sales(superstore_data)
    sorted_top_average_sales = get_top_average_sales(sorted_average_sales, k)
    return sorted_top_average_sales 


def get_average_sales(superstore_data):
    """Helper to calculate the average sales for each Region/Sub-Category pair."""
    group_data = defaultdict(lambda: {'Total Sales': 0.0, 'Count': 0})

    for row in superstore_data:
        key = (row.get('Region'), row.get('Sub-Category'))
        if key[0] and key[1]: # Ensure both region and sub-category exist
            group_data[key]['Total Sales'] += row.get('Sales', 0.0)
            group_data[key]['Count'] += 1

    average_sales = []
    for (region, subcategory), values in group_data.items():
        average = 0.0
        if values['Count'] > 0:
            average = values['Total Sales'] / values['Count']
        average_sales.append({'Region': region, 'Sub-Category': subcategory, 'Average Sales': average})
    
    # Sort by Region, then by Average Sales (desc), then Sub-Category (asc for tie-breaking)
    sorted_average_sales = sorted(average_sales, key=lambda x: (x['Region'], -x['Average Sales'], x['Sub-Category']))
    return sorted_average_sales

def get_top_average_sales(sorted_average_sales, k):
    """Helper to get the top k results for each region from a sorted list."""
    top_average_sales = []
    region_counts = defaultdict(int)
    
    for row in sorted_average_sales:
        region = row['Region']
        if region_counts[region] < k:
            top_average_sales.append(row)
            region_counts[region] += 1
            
    return top_average_sales


def write_csv(data_list, result_file, fieldnames):
    """Writes a list of dictionaries to a CSV file."""
    if not data_list:
        print(f"Warning: No data to write to {result_file}.")
        return

    with open(result_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data_list)
    print(f"Successfully wrote results to {result_file}")


def run_all_tests():
    """Runs all test cases for the project."""
    print("--- STARTING ALL TESTS ---")
    test_calc_region_profitability()
    test_calc_top_subcats_by_region()
    print("--- ALL TESTS FINISHED ---")

def test_calc_region_profitability():
    """Tests the calc_region_profitability function with general and edge cases."""
    print("\n--- Testing calc_region_profitability ---")

    # Test Case 1: Basic data
    data1 = [
        {'Region': 'East', 'Sales': 100.0, 'Profit': 20.0},
        {'Region': 'West', 'Sales': 150.0, 'Profit': 30.0},
        {'Region': 'East', 'Sales': 50.0, 'Profit': 5.0},
    ]
    result1 = calc_region_profitability(data1)
    # Sort results for consistent comparison
    result1.sort(key=lambda x: x['Region'])
    expected1 = [
        {'Region': 'East', 'Total Sales': 150.0, 'Total Profit': 25.0, 'Profit Margin': (25.0/150.0)*100},
        {'Region': 'West', 'Total Sales': 150.0, 'Total Profit': 30.0, 'Profit Margin': (30.0/150.0)*100},
    ]
    assert result1 == expected1, "Profitability - General Case 1 FAILED"
    print("✅ Profitability - General Case 1 PASSED")

    # Test Case 2: Data for a single region
    data2 = [
        {'Region': 'Central', 'Sales': 200.0, 'Profit': 40.0},
        {'Region': 'Central', 'Sales': 300.0, 'Profit': -50.0},
    ]
    result2 = calc_region_profitability(data2)
    expected2 = [{'Region': 'Central', 'Total Sales': 500.0, 'Total Profit': -10.0, 'Profit Margin': (-10.0/500.0)*100}]
    assert result2 == expected2, "Profitability - General Case 2 FAILED"
    print("✅ Profitability - General Case 2 PASSED")

    # Test Case 3: Zero sales for a region
    data3 = [{'Region': 'South', 'Sales': 0.0, 'Profit': 10.0}]
    result3 = calc_region_profitability(data3)
    expected3 = [{'Region': 'South', 'Total Sales': 0.0, 'Total Profit': 10.0, 'Profit Margin': 0.0}]
    assert result3 == expected3, "Profitability - Edge Case 1 (Zero Sales) FAILED"
    print("✅ Profitability - Edge Case 1 (Zero Sales) PASSED")

    # Test Case 4: Empty list input
    data4 = []
    result4 = calc_region_profitability(data4)
    expected4 = []
    assert result4 == expected4, "Profitability - Edge Case 2 (Empty Input) FAILED"
    print("✅ Profitability - Edge Case 2 (Empty Input) PASSED")

def test_calc_top_subcats_by_region():
    """Tests the calc_top_subcats_by_region function with general and edge cases."""
    print("\n--- Testing calc_top_subcats_by_region ---")
    
    # Test Case 1: More than k sub-categories in a region
    data1 = [
        {'Region': 'West', 'Sub-Category': 'Phones', 'Sales': 200.0},
        {'Region': 'West', 'Sub-Category': 'Chairs', 'Sales': 400.0},
        {'Region': 'West', 'Sub-Category': 'Tables', 'Sales': 600.0},
        {'Region': 'West', 'Sub-Category': 'Storage', 'Sales': 50.0},
        {'Region': 'West', 'Sub-Category': 'Copiers', 'Sales': 1000.0},
        {'Region': 'West', 'Sub-Category': 'Binders', 'Sales': 20.0},
    ]
    result1 = calc_top_subcats_by_region(data1, k=3)
    expected1 = [
        {'Region': 'West', 'Sub-Category': 'Copiers', 'Average Sales': 1000.0},
        {'Region': 'West', 'Sub-Category': 'Tables', 'Average Sales': 600.0},
        {'Region': 'West', 'Sub-Category': 'Chairs', 'Average Sales': 400.0},
    ]
    assert result1 == expected1, "Top Subcats - General Case 1 FAILED"
    print("✅ Top Subcats - General Case 1 PASSED")
    
    # Test Case 2: Test alphabetical tie-breaking
    data2 = [
        {'Region': 'East', 'Sub-Category': 'Tables', 'Sales': 500.0},
        {'Region': 'East', 'Sub-Category': 'Binders', 'Sales': 300.0}, # Same avg sales as Art
        {'Region': 'East', 'Sub-Category': 'Art', 'Sales': 300.0},     # Same avg sales as Binders
        {'Region': 'East', 'Sub-Category': 'Phones', 'Sales': 400.0},
    ]
    result2 = calc_top_subcats_by_region(data2, k=4)
    expected2 = [
        {'Region': 'East', 'Sub-Category': 'Tables', 'Average Sales': 500.0},
        {'Region': 'East', 'Sub-Category': 'Phones', 'Average Sales': 400.0},
        {'Region': 'East', 'Sub-Category': 'Art', 'Average Sales': 300.0}, # Art comes before Binders
        {'Region': 'East', 'Sub-Category': 'Binders', 'Average Sales': 300.0},
    ]
    assert result2 == expected2, "Top Subcats - General Case 2 (Tie-breaking) FAILED"
    print("✅ Top Subcats - General Case 2 (Tie-breaking) PASSED")

    # Test Case 3: Fewer than k sub-categories
    data3 = [
        {'Region': 'South', 'Sub-Category': 'Paper', 'Sales': 50.0},
        {'Region': 'South', 'Sub-Category': 'Envelopes', 'Sales': 100.0},
    ]
    result3 = calc_top_subcats_by_region(data3, k=5)
    expected3 = [
        {'Region': 'South', 'Sub-Category': 'Envelopes', 'Average Sales': 100.0},
        {'Region': 'South', 'Sub-Category': 'Paper', 'Average Sales': 50.0},
    ]
    assert result3 == expected3, "Top Subcats - Edge Case 1 (Fewer than k) FAILED"
    print("✅ Top Subcats - Edge Case 1 (Fewer than k) PASSED")

    # Test Case 4: Empty list input
    data4 = []
    result4 = calc_top_subcats_by_region(data4, k=5)
    expected4 = []
    assert result4 == expected4, "Top Subcats - Edge Case 2 (Empty Input) FAILED"
    print("✅ Top Subcats - Edge Case 2 (Empty Input) PASSED")


def main():
    # Define file paths
    input_file = 'data/SampleSuperstore 2.csv'
    profitability_output_file = 'result/region_profitability.csv'
    top_subcats_output_file = 'result/top_subcats_by_region.csv'
    
    # 1. Load data
    superstore_list = load_csv(input_file)
    
    # 2. Clean data
    superstore_data = clean_data(superstore_list)
    
    if superstore_data:
        # 3. Perform calculation 1 and write results
        profitability_data = calc_region_profitability(superstore_data)
        profit_fieldnames = ['Region', 'Total Sales', 'Total Profit', 'Profit Margin']
        write_csv(profitability_data, profitability_output_file, profit_fieldnames)
        
        # 4. Perform calculation 2 and write results
        top_subcats_data = calc_top_subcats_by_region(superstore_data, k=5)
        subcat_fieldnames = ['Region', 'Sub-Category', 'Average Sales']
        write_csv(top_subcats_data, top_subcats_output_file, subcat_fieldnames)
    else:
        print("Could not perform calculations because no data was loaded.")

if __name__ == "__main__":
    run_all_tests()

    main()
