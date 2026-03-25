import os

class SQLProvider:
    def __init__(self, file_path):
        self.scripts = {}
        for file in os.listdir(file_path):
            if file.endswith('.sql'):
                with open(os.path.join(file_path, file), 'r', encoding='utf-8') as f:
                    _sql = f.read()
                    self.scripts[file] = _sql  

    def get(self, name):
        return self.scripts.get(name, "") #просто возвращение .sql запроса в виде строки