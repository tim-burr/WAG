# Imports
# Local
import utils.drive_tools as drive

class Template:
    def __init__(self, dir):
        self._templates = {}
        self._files = drive.walk_dir(dir)
    
    # ****************
    # Public methods
    # ****************
    def open(self, templates: dict) -> None:
    # Open all essential templates for token replacement
        for name, path in templates.items():
            self.templates[name] = drive.open_file(path)
    
    def find(self, filename: str) -> dict:
    # Search if more specific template was requested
        try:
            path = self._files[filename]
            new = drive.open_file(path)
        except:
            print("Using default template")
            new = self.templates["default"]
        
        # TODO: Allow multiple returned content values
        self.templates["content"] = new # Rename content dict key to be standard no matter the page name

    @property
    def templates(self):
        return self._templates