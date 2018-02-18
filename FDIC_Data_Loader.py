import csv, os

class FDIC_Data_Loader(object):
    def __init__(self, data_dir, data_sheet_tuple, compiled_data_dir):
        '''takes directory location of data and list of dates in the format:
        YYYYMMDD'''    

        self.total_report = {}
        self.data_sheet_list = data_sheet_tuple[1]
        self.write_list = data_sheet_tuple[0]
        self._compiled_data_dir = compiled_data_dir
        for file in os.listdir(data_dir):
            #(20) chars up to date - (-4)'.csv' 
            if(file[20:-4] in self.data_sheet_list.keys()):
                print("Loading data for " + file[20:-4])
                self._load_data_(data_dir + file, file[20:-4])


                
    def _load_data_(self, file, data_sheet_type):
        with open(file, 'r') as csvfile:         
            csv_read = csv.reader(csvfile)
            #rip header and get indexes for desired data            
            header_list = next(csv_read)
            data_indexes = self._header_indexes_(header_list, data_sheet_type)
            
            for row in csv_read:
                for items in data_indexes.keys():
                    #check if cert been entered into total_report
                    if(not row[0] in self.total_report.keys()):
                        self.total_report.update({row[0] : dict()})
                    
                    for priority in data_indexes.keys():
                        self.total_report[row[0]].update({priority : row[data_indexes[priority]]})
            
            
        
            
    def _header_indexes_(self, header_list, sheet_list):
        indexes = {}
        for items in self.data_sheet_list[sheet_list].keys():
            try:
                indexes.update({items : header_list.index(items)})
            except:
                print(items + " not found in "+ sheet_list)        
        return indexes
        
    def generate_csv_header(self, write_list):
        proper_header = []      
        for item in write_list:
            for dicts in self.data_sheet_list.keys():
                if(item in self.data_sheet_list[dicts].keys()):
                    proper_header.append(self.data_sheet_list[dicts][item])
        
        return proper_header
    
    def generate_total_average(self):
        '''Generate total average of all data'''
        self.total_average = {"cert" : 999999, "name" : "institutions", "namehcr" : "Total Averages"}
        
        for item in self.write_list[3:]:
            self.total_average.update({item : 0})
        
        total_banks = 0
        for bank in self.total_report.keys():         
            index = 2
            if(self.total_report[bank]["asset"] == 0):
                continue
            total_banks+=1           
            for items in self.write_list[3:]:
                index+=1
                if(self.total_report[bank][items] == ""):
                    continue
                self.total_average[self.write_list[index]]+=float(self.total_report[bank][items])
        
        self.total_average["name"] = str(total_banks) + " institutions"
        
        for item in self.write_list[3:]:
            self.total_average[item] = self.total_average[item]/total_banks
        
        self.total_report.update({"Total Averages" : self.total_average})
      
    def calculate_average(self, cert_list, cert, custom_cert):
        self.custom_average = {"cert" : custom_cert, "name" : "institutions", "namehcr" : "Custom Average for cert" + str(cert)}
        
        for item in self.write_list[3:]:
            self.custom_average.update({item : 0})
        
        total_banks = 0
        if(len(cert_list)>100):
            include = 100
        else:
            include = len(cert_list)
            
        for bank in cert_list[0:include]:         
            index = 2
            if(self.total_report[bank]["asset"] == 0):
                continue
            total_banks+=1           
            for items in self.write_list[3:]:
                index+=1
                if(self.total_report[bank][items] == ""):
                    continue
                self.custom_average[self.write_list[index]]+=float(self.total_report[bank][items])
        
        self.custom_average["name"] = str(total_banks) + " institutions"
        
        for item in self.write_list[3:]:
            self.custom_average[item] = self.custom_average[item]/total_banks
        
        self.total_report.update({custom_cert : self.custom_average})
         
    def generate_custom_average(self, cert, custom_cert):
        similar_cert_list = []
        similar_asset_list = []
        
        top_loan = self.determine_top_loan_type(cert)
        for banks in self.total_report.keys():
            if(banks == cert):
                continue
            if(top_loan == self.determine_top_loan_type(banks)):
                similar_cert_list.append(banks)
                similar_asset_list.append(self.total_report[cert]["asset"])
        sorted_by_asset_certs = [similar_cert_list for _,similar_cert_list in sorted(zip(similar_asset_list,similar_cert_list))]
        self.calculate_average(sorted_by_asset_certs, cert, custom_cert)
        
                
        
        
    def determine_top_loan_type(self, cert):
        top_loan = 0
        top_loan_name = ""
        for loan_type in self.data_sheet_list["_Net Loans and Leases"].keys():
                        
            if(self.total_report[cert][loan_type] != "" and float(self.total_report[cert][loan_type])>top_loan):
                top_loan = float(self.total_report[cert][loan_type])
                top_loan_name = loan_type
        return(top_loan_name)
    
    def load_to_csv(self, desired_file_name):
        with \
        open(self._compiled_data_dir + \
        desired_file_name, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',')
            header_first = self.generate_csv_header(self.write_list)         
            csv_writer.writerow(header_first)
            csv_writer.writerow(list(range(1,len(header_first) + 1)))
            for certs in self.total_report.keys():
                data_list = []
                for item in self.write_list:
                    data_list.append(self.total_report[certs][item])
                csv_writer.writerow(data_list)




def convert_num_to_chars(integer):   
    '''takes int and returns column name within excel (A1 notation)'''    
    conversion = ""
    chars = ["","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P",\
    "Q","R","S","T","U","V","W","X","Y","Z"]
    if(integer > 26):
        conversion += chars[int(integer/26)]
        conversion += chars[integer%26]
    else:
        conversion += chars[integer]
    return conversion


def generate_data_sheet_list(directory):
        data_sheet_list = dict()        
        write_list = []        
        for file in os.listdir(directory):
            data_sheet_list.update({str(file[0:-4]) : dict()})
            with open(directory + file, 'r') as csvfile:
                csv_read = csv.reader(csvfile)
                for row in csv_read:
                    data_sheet_list[file[0:-4]].update({str(row[0]).rstrip() : str(row[1]).rstrip()})
                    write_list.append(row[0].rstrip())
        return((write_list, data_sheet_list))     

def generate_excel_functions(meta_data_list, current_row, base_column):
    vlookup = "VLOOKUP({},{},{},FALSE)"
    hlookup = "HLOOKUP({},{},{},FALSE)"
    sheet_cells = "'{}'{}"
    function_row = []    
    for c, date in enumerate(meta_data_list, base_column):
        function_row.append(vlookup.format("A1",\
        sheet_cells.format(date[1],date[2]), \
        hlookup.format(\
            ("A"+str(current_row+1)),\
            sheet_cells.format(date[1],date[3]),\
            2)))
    return function_row

    

def load_to_excel(excel_file_with_dir, compiled_data_location, data_list):
    from xlsxwriter.workbook import Workbook
    #Bank_Report_Generator (version 2).xlsx
    workbook = Workbook(excel_file_with_dir)
    sheet_list = []
    meta_data_list = []     
    for csvfile in os.listdir(compiled_data_location):
        sheet_list.append(csvfile[0:-4])
        print("Working on " + csvfile)    
        worksheet = workbook.add_worksheet(csvfile[0:-4]) #worksheet with csv file name
        with open(compiled_data_location +csvfile, 'r') as f:
            reader = csv.reader(f)
            row_count = 0
            for r, row in enumerate(reader):
                column_count = 0
                row_count += 1                
                for c, col in enumerate(row):
                    column_count += 1
                    if("." in col):
                        try:                
                            worksheet.write(r, c, float(col)) #write the csv file content into it
                        except:
                            worksheet.write(r, c, str(col))
                    elif(col.isdigit()):
                        worksheet.write(r,c,int(col))
                    else:
                        worksheet.write(r,c,str(col))
            column_1 = "{}/{}/{}".format(csvfile[4:6], csvfile[6:8],csvfile[0:4])
            column_2 = csvfile[0:-4]
            column_3 = \
            "!$A$1:${}${}".format(convert_num_to_chars(column_count),str(row_count))
            column_4 = "!$A$1:${}$2".format(convert_num_to_chars(column_count))
            meta_data_list.append([column_1, column_2, column_3, column_4])


    default = 999999 
    #all CSVFile data has been loaded. Load Meta data now    
    print("Working on Populating Dashboard Data Lookup")
    worksheet = workbook.add_worksheet("Dashboard Data")
    worksheet.write(0,0, default)
    for r, row in enumerate(meta_data_list, 1):
        for c, col in enumerate(row, 0):
            worksheet.write(c,r, col)

    #write data sheet items to excel
    base = 4
    for key in data_list.keys():
        for r, row in enumerate(data_list[key].keys(),base):        
            worksheet.write(r,0, data_list[key][row])
            function_row_list = generate_excel_functions(meta_data_list, r, 1)            
            for c, col in enumerate(function_row_list, 1):
                worksheet.write_formula(r,c,col)
            base += 1
            
        

              
    workbook.close()
        
def determine_custom_averages():
    avg_dir = os.path.dirname(os.path.realpath(__file__)) + "/average_certs.csv"
    avg_dict = {}    
    with open(avg_dir, 'r') as avg:
        avg_reader = csv.reader(avg)
        for row in avg_reader:
            avg_dict.update({row[0] : row[1]})
    return avg_dict
    

            
    


def main(directory_total_data, data_sheet_items_dir, excel_file_with_dir, compiled_bank_data_location):
    ''' 1. Takes Directory where All_Reports for multiple quarters are.
        2. Takes data_sheet_items_dir
        3. Takes Excel file name with dir
        4. Takes Condensed/Compiled CSV file location
    Loops through directory folders and creates FDIC_Bank_Data_Loader objects
        for each date. '''
    
    custom_avg_dict = determine_custom_averages()
    datasheet_tuple = generate_data_sheet_list(data_sheet_items_dir)
    for file in os.listdir(directory_total_data):
        print("Loading data from date: " + file[12:])

        current_date_loader = FDIC_Data_Loader(\
        directory_total_data + "/" + file + "/", \
        datasheet_tuple, \
        compiled_bank_data_location)
        
        current_date_loader.generate_total_average()
        
        for cert in custom_avg_dict.keys():
            current_date_loader.generate_custom_average(cert, custom_avg_dict[cert])
        
        current_date_loader.load_to_csv(file[12:] + ".csv")
    
    load_to_excel(\
    excel_file_with_dir, \
    compiled_bank_data_location,
    datasheet_tuple[1])
