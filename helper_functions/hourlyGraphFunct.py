
import pandas as pd
import inspect
from helper_functions.tripProp import tripProp
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import Qt

def load_excel(file_path, index):
    """Load data from Excel file with fixed headers and row titles"""
    options = QFileDialog.Options()
    
    if file_path:
        try:
            # Fixed parameters for the data section
            sheet_name = "GL-Sets"  
            start_row = 7   
            end_row = 30    
            start_col = 2+7*index  
            end_col = 7+7*index     
            
            # Fixed headers and row titles
            fixed_headers = ["Visitor -", "Visitor +", "Employee -", "Employee +", "Commercial -", "Commercial +"]
            fixed_row_titles = ["00:00 - 01:00", "01:00 - 02:00", "02:00 - 03:00", "03:00 - 04:00", "04:00 - 05:00", "05:00 - 06:00", "06:00 - 07:00", "07:00 - 08:00", "08:00 - 09:00", "09:00 - 10:00", "10:00 - 11:00", "11:00 - 12:00", "12:00 - 13:00", "13:00 - 14:00", "14:00 - 15:00", "15:00 - 16:00", "16:00 - 17:00", "17:00 - 18:00", "18:00 - 19:00", "19:00 - 20:00", "20:00 - 21:00", "21:00 - 22:00", "22:00 - 23:00", "23:00 - 24:00"]
            
            # Read the Excel file
            full_df = pd.read_excel(file_path, sheet_name=sheet_name)
            
            # Extract the specified section
            section_df = full_df.iloc[start_row:end_row+1, start_col:end_col+1].copy()
            
            # Apply fixed headers and row titles
            section_df.columns = fixed_headers
            section_df.index = fixed_row_titles
            
            return section_df
        except Exception as e:
            print(f"Error loading Excel file: {e}")
            # Return an empty DataFrame with the expected structure
            return pd.DataFrame(columns=fixed_headers)
        

def table_view_to_dataframe(table_view):
    # Get the model from the table view
    model = table_view.model()
    
    # Get row and column counts
    row_count = model.rowCount()
    column_count = model.columnCount()
    
    # Get header data if available
    headers = []
    for column in range(column_count):
        header_data = model.headerData(column, Qt.Horizontal)
        headers.append(str(header_data) if header_data is not None else f"Column {column}")
    
    # Extract data from the model
    data = []
    for row in range(row_count):
        row_data = []
        for column in range(column_count):
            # Get data for each cell
            index = model.index(row, column)
            cell_data = model.data(index)
            row_data.append(cell_data)
        data.append(row_data)
    
    # Create pandas DataFrame
    df = pd.DataFrame(data, columns=headers)
    return df



def calculateDataForGraph (hourlyData, chosenProps, tripType, meansIndex):
    totalTrips=None
    colSource=None

    if(tripType==0):
        colSource=0
    elif(tripType==1):
        colSource=2

    if isinstance(chosenProps, tripProp):
        if(meansIndex==0):
            totalTrips=chosenProps.pedestrianTrips
        elif(meansIndex==1):
            totalTrips=chosenProps.bikeTrips
        elif(meansIndex==2):
            totalTrips=chosenProps.publicTrips
        elif(meansIndex==3):
            totalTrips=chosenProps.motorTrips
    else:
        totalTrips=chosenProps
        colSource=4

    numeric_col = pd.to_numeric(hourlyData.iloc[:, colSource], errors='coerce')
    numeric_col_plus = pd.to_numeric(hourlyData.iloc[:, colSource+1], errors='coerce')
    
    # Create the result DataFrame
    result_df = pd.DataFrame()
    
    # Ensure totalTrips is a number before division
    if totalTrips is not None:
        # Calculate using the converted numeric columns
        result_df['Processed-'] = (numeric_col/100) * (totalTrips/2)
        result_df['Processed+'] = (numeric_col_plus/100) * (totalTrips/2)
    else:
        print("Error: totalTrips is None")
    
    return result_df