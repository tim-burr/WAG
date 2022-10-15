# Imports
# Standard
from pathlib import Path
# Third Party
import frontmatter
from markdown import markdown
from yattag import indent
# Local
from utils.drive_tools import *
from utils.config_loader import *
from utils.template_loader import *

class generator:
    def __init__(self, config: configuration, templates: template):
        self._homepage = config.homepage
        self._paths = config.paths
        self._tokens = config.tokens
        self._pretty = config.ispretty
        self._templates = templates
    
    # ****************
    # Private methods
    # ****************
    def _parse_page(self, page):
        # Split serialized YAML frontmatter from Markdown content
        with open(page) as f:
            metadata, content = frontmatter.parse(f.read())
        return metadata, content

    def _md_to_html(self, content):
        # Convert Markdown into HTML
        html = markdown(content)
        return html
    
    # ****************
    # Public methods
    # ****************
    def generate(self, page):
        # Instance variables
        build_dir = self._paths.get("build")
        page_name = Path(page).stem   # Filename w/o extension

        # Convert custom page into HTML
        metadata, content = self._parse_page(page)
        html_content = self._md_to_html(content)

        # Get page layout components from templates
        page_layout = metadata.get("template")
        layouts = self._templates.get_files(page_layout)
        
        # Define recognized in-page template tags
        params = {
            "{title}": metadata.get("title"),
            "{description}": metadata.get("description"),
            "{header}": layouts.get("header"),
            "{content}": html_content,
            "{footer}": layouts.get("footer")
         }
        params = params | self._tokens  # Append user-defined tokens

        # Set active nav menu button
        # Adds new dict key/value pair if needed
        category = metadata["category"]
        try:
            params[f"{{-{category}}}"] = "" # Remove token value to activate menu button
        except:
            print("No active menu links to update")

        # Populate tokens in template buffer
        html_doc = layouts.get("content")

        for key, value in params.items():
            if key in html_doc:
                html_doc = html_doc.replace(key, value)
        
        # Prettify HTML (compile option)
        if self._pretty:
            html_doc = indent(html_doc)
        
        # Determine final path of new page
        if page_name.isnumeric():
            # Numeric error page saves to build root
            build_subdir = build_dir
            new_file = (build_subdir / page_name).with_suffix(".html")
        elif page_name == self._homepage:
            # Homepage saves to build root
            build_subdir = build_dir
            new_file = build_subdir / "index.html"
        elif page_name == category:
            # Launch page saves near top of directory
            build_subdir = build_dir / page_name
            new_file = build_subdir / "index.html"
        else:
            # Default: Child page gets their own subfolder
            build_subdir = build_dir / category / page_name
            new_file = build_subdir / "index.html"
       
        # Create directory to store new page, if does not exist
        create_directory(build_subdir)

        # Save HTML buffer to new file
        with open(new_file, 'w') as f:
            f.write(html_doc)

        print("Page generated")