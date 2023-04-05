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
                temp = name                
                path = self._files[temp]  # Try finding block path for first time by name
            except KeyError:
                print("Data not found, using default")
                temp = self._default
                path = self._files.get(temp)  # Find default block path by name
            finally:
                self.blocks[temp] = drive.read_file(path)  # Load content from disk
                block = self.blocks[temp]
        finally:
            return block

    def all(self) -> None:
        for k,v in self._files.items():
            self.blocks[k] = drive.read_file(v)

    @property
    def blocks(self) -> dict:
        return self._blocks