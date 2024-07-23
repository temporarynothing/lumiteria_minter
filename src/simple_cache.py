import os
import json

class SimpleCache:
    def __init__(self, key):
        self.key = key
        self.load()

    def file_path(self):
        return f'../data/{self.key}.json'

    def load(self):
        if os.path.exists(self.file_path()):
            try:
                with open(self.file_path(), 'r') as f:
                    self.data = json.load(f)
            except json.JSONDecodeError:
                self.data = {}
        else:
            self.data = {}

    def save(self):
        with open(self.file_path(), 'w') as f:
            json.dump(self.data, f, indent=4)

    def set(self, key, value):
        self.data[key] = value
        self.save()

    def get(self, key):
        return self.data.get(key)

    def exists(self, key):
        return key in self.data

    def clear(self):
        self.data = {}
        self.save()

    def is_empty(self):
        return not self.data
