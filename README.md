Written with Python 3.5.2

# FDIC-Bank-Data-Organizer
Main takes 4 dir locations
        1. Takes Directory where All_Reports for multiple quarters are.
        2. Takes data_sheet_items_dir
        3. Takes Excel file name with dir
        4. Takes location where Condensed/Compiled CSV files will be stored. (Needs to be empty for first run)

Example Output of Python Script:
>main("C:/Users/wyatt/Desktop/FDIC-Bank-Data-Organizer-master/All_Reports/",\
>       "C:/Users/wyatt/Desktop/FDIC-Bank-Data-Organizer-master/data_sheet_items/",\
>        "C:/Users/wyatt/Desktop/FDIC-Bank-Data-Organizer-master/Compiled_Data.xlsx",\
>        "C:/Users/wyatt/Desktop/FDIC-Bank-Data-Organizer-master/Compiled_Files/")
>        Loading data from date: 20180630
>        Loading data for _Assets and Liabilities
>        Loading data for _Income and Expense
>        Loading data for _Net charge-offs to loans
>        Loading data for _Net Loans and Leases
>        Loading data for _Noncurrent loans to loans
>        Loading data for _Performance and Condition Ratios
>        rbc1rwaj not found in _Performance and Condition Ratios
>        Loading data from date: 20181231
>        Loading data for _Assets and Liabilities
>        Loading data for _Income and Expense
>        Loading data for _Net charge-offs to loans
>        Loading data for _Net Loans and Leases
>        Loading data for _Noncurrent loans to loans
>        Loading data for _Performance and Condition Ratios
>        rbc1rwaj not found in _Performance and Condition Ratios
>        Loading data from date: 20190331
>        Loading data for _Assets and Liabilities
>        Loading data for _Income and Expense
>        Loading data for _Net charge-offs to loans
>        Loading data for _Net Loans and Leases
>        Loading data for _Noncurrent loans to loans
>        Loading data for _Performance and Condition Ratios
>        rbc1rwaj not found in _Performance and Condition Ratios
>        Loading data from date: 20190630
>        Loading data for _Assets and Liabilities
>        Loading data for _Income and Expense
>        Loading data for _Net charge-offs to loans
>        Loading data for _Net Loans and Leases
>        Loading data for _Noncurrent loans to loans
>        Loading data for _Performance and Condition Ratios
>        rbc1rwaj not found in _Performance and Condition Ratios
>        Loading data from date: 20190930
>        Loading data for _Assets and Liabilities
>        Loading data for _Income and Expense
>        Loading data for _Net charge-offs to loans
>        Loading data for _Net Loans and Leases
>        Loading data for _Noncurrent loans to loans
>        Loading data for _Performance and Condition Ratios
>        rbc1rwaj not found in _Performance and Condition Ratios
>        Loading data from date: 20191231
>        Loading data for _Assets and Liabilities
>        Loading data for _Income and Expense
>        Loading data for _Net charge-offs to loans
>        Loading data for _Net Loans and Leases
>        Loading data for _Noncurrent loans to loans
>        Loading data for _Performance and Condition Ratios
>        rbc1rwaj not found in _Performance and Condition Ratios
>        Loading data from date: 20200331
>        Loading data for _Assets and Liabilities
>        Loading data for _Income and Expense
>        Loading data for _Net charge-offs to loans
>        Loading data for _Net Loans and Leases
>        Loading data for _Noncurrent loans to loans
>        Loading data for _Performance and Condition Ratios
>        rbc1rwaj not found in _Performance and Condition Ratios
>        Working on importing data to excel for 20180630.csv
>        Working on importing data to excel for 20181231.csv
>        Working on importing data to excel for 20190331.csv
>        Working on importing data to excel for 20190630.csv
>        Working on importing data to excel for 20190930.csv
>        Working on importing data to excel for 20191231.csv
>        Working on importing data to excel for 20200331.csv
>        Working on Populating Dashboard Data Lookup


End Goal for this project is to provide easily accessible insights into: 
  Individual bank health over time
  Total systematic risk within the US markets
