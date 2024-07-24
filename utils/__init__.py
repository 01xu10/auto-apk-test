from common import ensure_path_sep
from utils.other_tools.model import Config
from utils.read_files_tools.yaml_control import GetYamlData

_data = GetYamlData(ensure_path_sep("\\resources\\config.yaml")).get_yaml_data()
Config.update_forward_refs()
config = Config(**_data)
