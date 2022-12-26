import requests
from my_token import TOKEN #импортируйте токен из файла; мой был my_token.py в папке с проектом

class YaUploader:
    URL_FILES_LIST: str = 'https://cloud-api.yandex.net/v1/disk/resources/files'
    URL_UPLOAD_LINK: str = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
    def __init__(self, token: str):
        self.token = token


    @property
    def header(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"OAuth {self.token}"
        }
        
        
    def get_files_list(self):
        response = requests.get(self.URL_FILES_LIST, headers=self.header)
        return response.json()
    
    
    def _get_upload_link(self, ya_disk_path: str):
        params = {"path": ya_disk_path, "overwrite": "true"}
        response = requests.get(self.URL_UPLOAD_LINK, headers=self.header, params=params)
        upload_url = response.json().get("href")
        return upload_url
        
        
    def upload(self, path_to_file: str):
        file_name = path_to_file.strip().split('\\')[-1]
        upload_link = self._get_upload_link(file_name)
        with open(path_to_file, 'rb') as file_obj:
            response = requests.put(upload_link, data=file_obj)
            if response.status_code == 201:
                print ("Файл успешно загружен!")
        return response.status_code


if __name__ == '__main__':
    path_to_file = input('Введите путь до файла: ')
    token = TOKEN
    uploader = YaUploader(token)
    result = uploader.upload(path_to_file)