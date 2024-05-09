import pandas as pd
from data.repositories import FileRepository
from io import BytesIO
from base64 import b64decode
import sqlite3
import re

class LibraryReaderService:
    def __init__(self, file_repository: FileRepository):
        self.file_repository:FileRepository = file_repository


    def library_reader(self, function_name, **kwargs):

        file = self.file_repository.get_file_content_by_function_name(function_name=function_name)
        if not file:
            return "Error: File not found or empty."

        # Decode bytea and Load the relevant table into a dataFrame
        decoded_content_bytes = b64decode(file.content)
        data_type = file.file_extension.lower()
        library = BytesIO(decoded_content_bytes)

        if data_type in ['csv', 'xlsx']:
            data_frame = None
            if data_type == 'csv':
                data_frame = pd.read_csv(library, encoding='utf-8')
            elif data_type == 'xlsx':
                data_frame = pd.read_excel(library)           
            return self.table_reader(data_frame, **kwargs)
        
        elif data_type == 'txt':
            file_content = decoded_content_bytes.decode('utf-8')
            return self.txt_reader(file_content, **kwargs)
        
        elif data_type == 'web service':
            return self.web_service_reader(function_name = function_name, library = library, **kwargs)

        return f"Unsupported file type: {data_type}"



    def table_reader(self, data_frame, **kwargs):

            if not kwargs:
                # Check if the number of rows is shorter than or equal to 20
                if len(data_frame) <= 500:
                    # Return the whole CSV
                    csv_output = data_frame.to_csv(index=False, header=True, encoding='utf-8')
                    return csv_output
                else:
                    csv_output = data_frame.head(500).to_csv(index=False, header=True, encoding='utf-8')
                    return csv_output
            # GPT might return keys with '?' if it's not sure.
            kwargs = {k.rstrip('?'): v for k, v in kwargs.items()}
            # Validate the provided arguments
            valid_columns = data_frame.columns.tolist()
            for key in kwargs.keys():
                if key not in valid_columns:
                    return f"Error: Invalid column name '{key}'"

            relavant_data = data_frame
                # Filter the rows based on the provided arguments
            try:
                for key, value in kwargs.items():
                    if key in relavant_data.columns and pd.api.types.is_numeric_dtype(relavant_data[key]):
                        # Check if the column is numeric, then filter with numeric comparison
                        condition = relavant_data[relavant_data[key] == int(value)]   
                    else:
                        # For non-numeric columns, use string contains as before
                        condition = relavant_data[relavant_data[key].astype(str).str.contains(str(value), case=False, na=False)]

                    relavant_data = condition                 

                if relavant_data.empty:
                    return "No Outcome Returned"                
                else:
                    return relavant_data.to_csv(index=False, header=True, encoding='utf-8')

            except KeyError:
                return "Error: Invalid column name or value"


    def txt_reader(self, file_content, **kwargs):
        
        if not kwargs:
            return file_content
        results = {}
        # Process the content line by line
        for line in file_content.split('\n'):
            for pattern_name, pattern in kwargs.items():
                if pattern_name not in results:
                    results[pattern_name] = []

                match = re.search(pattern, line)
                if match:
                    results[pattern_name].append(match.group(1))

        return results


    def web_service_reader(self, function_name, library, **kwargs):
        data_frame = pd.read_csv(library, encoding='utf-8')
        self.create_sqlite_table(function_name=function_name, data_frame=data_frame)
        # Create an SQLite connection
        conn = sqlite3.connect('databases'+f'{function_name}.db')
        sql_query = kwargs["query"]
        try:
            result = pd.read_sql_query(sql_query, conn)
        except Exception as e:
            result = e
        conn.close()
        return result.to_csv(index=False, header=True, encoding='utf-8')


    def create_sqlite_table(self, function_name, data_frame):
        # Create an SQLite database and save the dataFrame as a table
        conn = sqlite3.connect('databases'+f'{function_name}.db')
        data_frame.to_sql('tours', conn, if_exists='replace', index=False)
        # Commit and close the connection
        conn.commit()
        conn.close()
        return "SQLite table 'table' created successfully."
