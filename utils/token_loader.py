# Imports

class Token():
    def __init__(self, tokens: dict):
        self._tokens = {}
        self._tokens = self.addt(tokens)

    # ****************
    # Private methods
    # ****************
    @staticmethod
    def _format(keys: list) -> list:
        formatted = [f"{{{id}}}" for id in keys]
        return formatted

    # ****************
    # Public methods
    # ****************
    def addt(self, tokens: dict) -> dict:
        # Can't use unzip because of one-element dictionaries
        keys = tokens.keys()
        values = tokens.values()

        keys = self._format(keys)  # Format the keys with custom parse characters
        new = dict(zip(keys, values))  # Combine new keys with existing values
        self.tokens.update(new)  # Overwrites entries with latest token definitions
        return self.tokens

    @property
    def tokens(self) -> dict:
        return self._tokens