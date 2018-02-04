#Bank data via data extracted here: 
#    https://www5.fdic.gov/sdi/main.asp?formname=compare
#bank health reports        
#https://www5.fdic.gov/sdi/Resource/AllReps/All_Reports_20170630.zip
"""
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
    
    def generate_average(self):
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


def load_to_excel(excel_file_with_dir, compiled_data_location):
    from xlsxwriter.workbook import Workbook
    #Bank_Report_Generator (version 2).xlsx
    workbook = Workbook(excel_file_with_dir)

    for csvfile in os.listdir(compiled_data_location):
        print("Working on " + csvfile)    
        worksheet = workbook.add_worksheet(csvfile[0:-4]) #worksheet with csv file name
        with open(compiled_data_location +csvfile, 'r') as f:
            reader = csv.reader(f)
            for r, row in enumerate(reader):
                for c, col in enumerate(row):
                
                    if("." in col):
                        try:                
                            worksheet.write(r, c, float(col)) #write the csv file content into it
                        except:
                            worksheet.write(r, c, col)
                    elif(col.isdigit()):
                        worksheet.write(r,c,int(col))
                    else:
                        worksheet.write(r,c,col)
                    
                    
        workbook.close()

def main(directory_total_data, data_sheet_items_dir, excel_file_with_dir, compiled_bank_data_location):
    ''' 1. Takes Directory where All_Reports for multiple quarters are.
        2. Takes data_sheet_items_dir
        3. Takes Excel file name with dir
        4. Takes Condensed/Compiled CSV file location
    Loops through directory folders and creates FDIC_Bank_Data_Loader objects
        for each date. '''
    for file in os.listdir(directory_total_data):
        print("Loading data from date: " + file[12:])

        current_date_loader = FDIC_Data_Loader(\
        directory_total_data + "/" + file + "/", \
        generate_data_sheet_list(data_sheet_items_dir), \
        compiled_bank_data_location)
        
        current_date_loader.generate_average()
        current_date_loader.load_to_csv(file[12:] + ".csv")
    
    load_to_excel(\
        excel_file_with_dir, \
        compiled_bank_data_location)
