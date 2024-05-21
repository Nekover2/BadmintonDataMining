import requests

def upload_to_pixeldrain(file_path):
    url = "https://pixeldrain.com/api/file"
    files = {'file': open(file_path, 'rb')}
    
    try:
        response = requests.post(url, files=files)
        response.raise_for_status()
        
        # Parse the JSON response
        response_data = response.json()
        
        # Extract the file ID and URL
        file_id = response_data.get('id')
        file_url = f"https://pixeldrain.com/u/{file_id}"
        
        return file_url
    
    except requests.exceptions.RequestException as e:
        print(f"Error uploading file: {e}")
        return None