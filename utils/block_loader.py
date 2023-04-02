# Imports
# Local
import utils.drive_tools as drive

class Block:
    def __init__(self, dir, default=''):
        self._blocks = {}
        self._files = drive.walk_dir(dir)
        self._default = default

    # ****************
    # Public methods
    # ****************
    def find(self, name: str) -> str:
        # Search and load content as needed
        try:
            block = self.blocks[name]  # Check if block was previously loaded
        except KeyError:
            try:
                path = self._files[name]  
                self.blocks[name] = drive.read_file(path)  # Try loading content from disk
                block = self.blocks[name]
            except KeyError:
                print("Data not found, using default")
                block = self.blocks[self._default]
        finally:
            return block

    def all(self) -> None:
        for k,v in self._files.items():
            self.blocks[k] = drive.read_file(v)

    @property
    def blocks(self) -> dict:
        return self._blocks