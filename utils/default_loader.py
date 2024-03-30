class Default():
    def __init__(self, defaults: dict):
        self.defaults = defaults

    # ****************
    # Public methods
    # ****************
    def substitute(self, tokens: dict) -> dict:
        for k,v in tokens.items():
            if v == 'default':
                tokens[k] = self.defaults.get(k)  # Only update if key matches
        return tokens