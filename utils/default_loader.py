# Imports

class Default():
    def __init__(self, defaults: dict):
        self._defaults = defaults
    
    # ****************
    # Public methods
    # ****************
    def substitute(self, tokens: dict) -> dict:
        for k,v in tokens.items():
            if v == 'default':
                tokens[k] = self.defaults.get(k)  # Only update if key matches
        return tokens
    
    @property
    def defaults(self) -> dict:
        return self._defaults