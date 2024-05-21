from Utils.FileUploader import upload_to_pixeldrain
from Utils.Mongodb import MongoDB
import json
class DataManager :
    def __init__(self, database_url, databaseName) -> None:
        self.database_url = database_url
        self.db = MongoDB(database_url, databaseName)
    @staticmethod
    def upload_needed_files(file_path):
        file_link = upload_to_pixeldrain(file_path)
        return file_link
    @staticmethod
    def read_json_file( file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    
    def store_to_database(self,document, collection_name):
        old_document = self.db.find_one(collection_name, {'input_file_link': document['input_file_link']})
        if old_document:
            self.db.update_one(collection_name, {'input_file_link': document['input_file_link']}, document)
        else:
            self.db.insert_one(collection_name, document)
            
    