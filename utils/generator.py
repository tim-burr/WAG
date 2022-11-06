# Imports
# Standard
from pathlib import Path
# Third Party
import frontmatter
from markdown import markdown
from yattag import indent
# Local
import utils.drive_tools as drive
import utils.config_loader as cfg

        self._tokens = config.tokens
class Generator:
    def __init__(self, config: cfg.Configuration):
        self._config = config
    
    # ****************
    # Private methods
    # ****************
    def _parse_page(self, page):
        # Split serialized YAML frontmatter from Markdown content
        with open(page) as f:
            metadata, content = frontmatter.parse(f.read())
        return metadata, content

    def _md_to_html(self, content) -> None:
        # Convert Markdown into HTML; Markdown inside HTML block tags allowed
        html = markdown(content, extensions=['md_in_html'])
        return html
    
    def _generate_from_md(self, page) -> None:
        # Instance variables
        build_dir = self._config.paths.get("build")
        page_name = Path(page).stem  # Filename w/o extension

        # Convert custom page into HTML
        metadata, content = self._parse_page(page)
        html_content = self._md_to_html(content)

         # Get page layout components from templates
        page_layout = metadata.get("template")
        layouts = self._config.find_template(page_layout)

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
            params[f"{{-{category}}}"] = ""  # Remove token value to activate menu button
        except:
            print("No active menu links to update")

        # Populate tokens in template buffer
        html_doc = layouts.get("content")

        for key, value in params.items():
            if key in html_doc:
                html_doc = html_doc.replace(key, value)

        # Prettify HTML (compile option)
        if self._config.ispretty:
            html_doc = indent(html_doc)
        
        # Determine final path of new page
        if page_name.isnumeric():
            # Numeric error page saves to build root
            build_subdir = build_dir
            new_file = (build_subdir / page_name).with_suffix(".html")
        elif page_name == self._config.homepage:
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
        drive.create_directory(build_subdir)

        # Save HTML buffer to new file
        with open(new_file, 'w') as f:
            f.write(html_doc)

        return html_doc

    def _generate_from_html(self, page) -> str:
        # TODO: Implement direct html file handling
        html_doc: str
        return html_doc
    
    # ****************
    # Public methods
    # ****************
    def generate(self, page) -> None:      
        # Handle input file type
        match page.suffix:
            case ".md":
                self._generate_from_md(page)
            case ".html":
                self._generate_from_html(page)
            case _:
                return

        print(f'Generate: "{page.stem}" page')