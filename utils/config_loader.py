# Imports
# Standard
from pathlib import Path
# Third Party
import yaml
# Local
import utils.default_loader as dft
import utils.block_loader as bok
import utils.token_loader as tok

# Script configuration manager
class Configuration:
    def __init__(self, file):
        self._config = self._open_config(file)
        self._defaults = self._load_defaults()
        self._paths = self._load_structure("paths")
        self._includes = self._load_structure("includes")
        self._templates = self._load_templates()
        self._modules = self._load_modules()
        self._tokens = self._load_tokens("tokens")
    
    # ****************
    # Private methods
    # ****************
    def _open_config(self, file) -> dict:
        with open(file, 'r') as f:
            loaded = yaml.safe_load(f)
        print("Build configuration loaded")
        return loaded

    def _load_structure(self, key: str) -> dict | list | None:       
        paths = self.config.get(key)

        # Determine iterable type
        if isinstance(paths, dict):
            collection = paths.items()
        elif isinstance(paths, list):
            collection = enumerate(paths)
        else:
            print("Invalid configuration data structure")
            return
        
        # Resolve all relative file paths
        for i, path in collection:
            paths[i] = Path(self.root) / path
        return paths
    
    def _load_defaults(self) -> dft.Default:
        defaults = self.config.get("defaults")
        defaults = dft.Default(defaults)
        return defaults

    def _load_block(self, path, default='') -> bok.Block:
        dir = self.paths.get(path)
        block = bok.Block(dir, default)
        return block

    def _load_templates(self) -> bok.Block:
        default = self.defaults.defaults.get("template")
        templates = self._load_block("templates", default)
        return templates
    
    def _load_modules(self) -> tok.Token:
        modules = self._load_block("modules")
        modules.all()
        modules = tok.Token(modules.blocks)
        return modules
    
    def _load_tokens(self, key: str) -> tok.Token:
        tokens = self.config.get(key)
        tokens = tok.Token(tokens)
        return tokens
    
    # ****************
    # Public methods
    # ****************   
    @property
    def config(self) -> dict:
        return self._config

    @property
    def root(self) -> dict:
        return self.config.get("root")

    @property
    def domain(self) -> dict:
        return self.config.get("domain")

    @property
    def homepage(self) -> dict:
        return self.config.get("homepage")

    @property
    def paths(self) -> dict:
        return self._paths

    @property
    def includes(self) -> list:
        return self._includes

    @property
    def templates(self) -> bok.Block:
        return self._templates

    @property
    def modules(self) -> tok.Token:
        return self._modules

    @property
    def tokens(self) -> tok.Token:
        return self._tokens

    @property
    def defaults(self) -> dft.Default:
        return self._defaults
    
    @property
    def ispretty(self) -> bool:
        return self.config.get("html_pretty")