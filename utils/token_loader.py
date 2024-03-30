class Token():
    def __init__(self, tokens: dict):
        self.tokens = {}
        self.tokens = self.addt(tokens)

    # ****************
    # Private methods
    # ****************
    def _format(self, keys: list) -> list:
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