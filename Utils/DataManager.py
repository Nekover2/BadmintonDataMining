from Utils.FileUploader import upload_to_pixeldrain
from Utils.Mongodb import MongoDB
class DataManager :
    def __init__(self, database_url) -> None:
        self.database_url = database_url
        self.db = MongoDB(database_url, 'data_manager')
    
    @staticmethod 
    def upload_needed_files(input_file, output_file):
        input_file_link = upload_to_pixeldrain(input_file)
        output_file_link = upload_to_pixeldrain(output_file)
        
    def store_to_database(self,document, collection_name):
        old_document = self.db.find_one(collection_name, {'input_file_link': document['input_file_link']})
        if old_document:
            self.db.update_one(collection_name, {'input_file_link': document['input_file_link']}, document)
        else:
            self.db.insert_one(collection_name, document)