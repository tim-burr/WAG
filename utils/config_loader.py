# Imports
# Standard
from pathlib import Path
# Third Party
import yaml
# Local
import utils.template_loader as tpl
import utils.token_loader as tok

# Script configuration manager
class Configuration:
    def __init__(self, file):
        self._config = self._open_config(file)
        self._templates = self._load_templates()
    
    # ****************
    # Private methods
    # ****************
    def _open_config(self, file) -> dict:
        with open(file, 'r') as f:
            loaded = yaml.safe_load(f)
        print("Build configuration loaded")
        return loaded

    def _get_structure(self, key: str, base = '') -> dict | list | None:
        paths = self.config.get(key)
        
        # Determine variable type
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
    
    def _load_templates(self) -> tpl.Template:
        paths = self.paths.get("templates")
        required = self._get_structure("templates", paths)
        templates = tpl.Template(paths)
        templates.open(required)
        return templates

    
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
    def includes(self):
        return self._get_structure("includes")

    @property
    def tokens(self):
        return self.config.get("tokens")

    @property
    def ispretty(self):
        return self.config.get("html_pretty")

    def find_template(self, name):
        self._templates.find(name)
        return self._templates.templates

    def add_tokens(self, **tokens):
        added_tokens = self._tokens.add_tokens(tokens)
        self._tokens
        pass