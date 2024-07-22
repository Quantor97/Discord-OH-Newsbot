import json
import os

class ServerSettings:
    def __init__(self, file_path='./cache/settings.json'):
        self.file_path = file_path
        self.settings = self.load_settings()

    def load_settings(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                return json.load(file)
        return {}

    def save_settings(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.settings, file, indent=4)

    def get_channel(self, guild_id):
        return self.settings.get(str(guild_id), {}).get('channel_id')

    def set_channel(self, guild_id, channel_id):
        if str(guild_id) not in self.settings:
            self.settings[str(guild_id)] = {}

        self.settings[str(guild_id)]['channel_id'] = channel_id
        self.save_settings()
