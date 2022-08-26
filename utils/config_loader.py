# Imports
from pathlib import Path
import yaml

# Script configuration manager
class configuration:
    def __init__(self, file):
        self._config = self._open_config(file)
    
    # ****************
    # Private methods
    # ****************
    def _open_config(self, file):
        with open(file, 'r') as f:
            loaded = yaml.safe_load(f)
        print("Build configuration loaded")
        return loaded

    def _get_structure(self, key: str, base = ''):
        paths = self._config.get(key)
        
        if isinstance(paths, dict):
            collection = paths.items()
        elif isinstance(paths, list):
            collection = enumerate(paths)
        else:
            return
        
        # Resolve all relative file paths
        for index, value in collection:
            paths[index] = Path(self.get_root()) / base / value 
        return paths
    
    # ****************
    # Public methods
    # ****************
    def get_config(self):
        return self._config

    def get_root(self):
        return self._config.get("root")

    def get_domain(self):
        return self._config.get("domain")

    def get_homepage(self):
        return self._config.get("homepage")

    def get_paths(self):
        return self._get_structure("paths")
    
    def get_templates(self, path = ''):
        return self._get_structure("templates", path)

    def get_includes(self, path = ''):
        return self._get_structure("includes", path)

    def get_tokens(self):
        return self._config.get("tokens")

    def get_pretty(self):
        return self._config.get("html_pretty")