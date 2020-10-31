import json, os

default_settings_dict = {
    "auto_walrus": True,
    "convert_hex": False,
    "convert_binary": False,
    "log_py_code": False

}

class Settings:
    settings_path: str

    auto_walrus: bool
    convert_hex: bool
    convert_binary: bool
    log_py_code: bool


    def __init__(self, load_path):
        self.settings_path = load_path
        self.load()

    def __repr__(self):
        out_str = "\n"

        for key, value in self.to_dict().items():
            out_str += f"{key}: {value}\n"

        return out_str

    def save(self):
        self.to_json_file()

    def to_dict(self) -> dict:
        out_dict = {}
        for key, value in default_settings_dict.items():
            out_dict[key] = self.__dict__[key]

        return out_dict

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=4, sort_keys=True)

    def to_json_file(self):
        json.dump(self.to_dict(), open(self.settings_path, 'w'), indent=4, sort_keys=True)



    def load(self):
        if not os.path.isfile(self.settings_path):
            self.from_dict(default_settings_dict)

        else:
            self.from_json_file()

    def from_dict(self, in_dict: dict):
        for key, value in default_settings_dict.items():
            if key not in in_dict:
                self.__dict__[key] = value
            else:
                self.__dict__[key] = in_dict[key]

    def from_json(self, json_str: str):
        self.from_dict(json.loads(json_str))

    def from_json_file(self):
        if os.path.exists(self.settings_path) and os.path.isfile(self.settings_path):
            self.from_dict(json.load(open(self.settings_path, 'r')))

