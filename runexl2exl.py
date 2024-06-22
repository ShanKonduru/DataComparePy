import pandas as pd
from pandasql import sqldf
from ExcelFile import ExcelFile
import ExcelDataComparator

# Example usage:
if __name__ == "__main__":
    # source_file_path = r'C:/MyProjects/DataComparePy/InputFiles/CSV/Src/SrcEmpData.xlsx'
    # target_file_path = r'C:/MyProjects/DataComparePy/InputFiles/CSV/Dest/DestEmpData.xlsx'
    source_file_path = r'C:/MyProjects/DataComparePy/InputFiles/CSV/Src/SrcTest.xlsx'
    target_file_path = r'C:/MyProjects/DataComparePy/InputFiles/CSV/Dest/DestTest.xlsx'

    sheet_name = 'Sheet1'  # Update with your sheet name
    
    # SQL query to select relevant columns for comparison
    src_query = "SELECT  EmpID as ID , EmpName as NAME, EmpAge as AGE, EmpSex as SEX, EmpSalary as SALARY  FROM df"
    dest_query = "SELECT Emp_ID as ID , Emp_Name as NAME, Emp_Age as AGE, Emp_Sex as SEX, Emp_Salary as SALARY FROM df"

    # Create an instance of ExcelDataComparator
    data_comparator = ExcelDataComparator.ExcelDataComparator(source_file_path, target_file_path, sheet_name)
    
    # Compare Excel with Excel using SQL query
    result_excel_excel = data_comparator.compare_excel_with_excel(src_query, dest_query)
    print(result_excel_excel)
