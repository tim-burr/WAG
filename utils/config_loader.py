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
        paths = self.config.get(key)
        
        if isinstance(paths, dict):
            collection = paths.items()
        elif isinstance(paths, list):
            collection = enumerate(paths)
        else:
            print("Invalid configuration data structure")
            return
        
        # Resolve all relative file paths
        for i, value in collection:
            paths[i] = Path(self.root) / base / value 
        return paths
    
    # ****************
    # Public methods
    # ****************
    @property
    def config(self):
        return self._config

    @property
    def root(self):
        return self.config.get("root")

    @property
    def domain(self):
        return self.config.get("domain")

    @property
    def homepage(self):
        return self.config.get("homepage")

    @property
    def paths(self):
        return self._get_structure("paths")
    
    @property
    def templates(self, path = ''):
        return self._get_structure("templates", path)

    @property
    def includes(self, path = ''):
        return self._get_structure("includes", path)

    @property
    def tokens(self):
        return self.config.get("tokens")

    @property
    def ispretty(self):
        return self.config.get("html_pretty")