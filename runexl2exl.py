import pandas as pd
from pandasql import sqldf
from ConfigLoader import ConfigLoader
from ExcelDataComparator import ExcelDataComparator

if __name__ == "__main__":
    # Load configuration from JSON file
    config_loader = ConfigLoader('config.json')
    config = config_loader.get_config()
    
    source_file_path = config["source_file_path"]
    target_file_path = config["target_file_path"]
    sheet_name = config["sheet_name"]
    src_query = config["src_query"]
    dest_query = config["dest_query"]
    
    # Create an instance of ExcelDataComparator
    data_comparator = ExcelDataComparator(source_file_path, target_file_path, sheet_name)
    
    # Compare Excel with Excel using SQL query
    result_excel_excel = data_comparator.compare_excel_with_excel(src_query, dest_query)
    print(result_excel_excel)

import pandas as pd
from pandasql import sqldf
from ConfigLoader import ConfigLoader
from ExcelDataComparator import ExcelDataComparator

if __name__ == "__main__":
    # Load configuration from JSON file
    config_loader = ConfigLoader('config.json')
    
    # Get all dataset names (IDs)
    dataset_ids = config_loader.get_all_dataset_names()
    
    for dataset_id in dataset_ids:
        print(f"Processing dataset: {dataset_id}")
        try:
            # Get the configuration for the specified dataset
            config = config_loader.get_config_by_id(dataset_id)
        except ValueError as e:
            print(e)
            continue  # Skip to the next dataset
        
        source_file_path = config["source_file_path"]
        target_file_path = config["target_file_path"]
        sheet_name = config["sheet_name"]
        src_query = config["src_query"]
        dest_query = config["dest_query"]
        
        # Create an instance of ExcelDataComparator
        data_comparator = ExcelDataComparator(source_file_path, target_file_path, sheet_name)
        
        # Compare Excel with Excel using SQL query
        result_excel_excel = data_comparator.compare_excel_with_excel(src_query, dest_query)
        
        # Output results
        print(f"Differences for dataset {dataset_id}:")
        print(result_excel_excel)
