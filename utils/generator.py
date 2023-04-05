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

class Generator:
    def __init__(self, config: cfg.Configuration):
        self._config = config
    
    # ****************
    # Private methods
    # ****************
    def _parse_page(self, page) -> tuple[dict, str]:
        # Split serialized YAML frontmatter from Markdown content
        with open(page) as f:
            metadata, content = frontmatter.parse(f.read())
        return metadata, content

    def _replace_tags(self, doc, tags: dict) -> str:
        for key, value in tags.items():
            doc = doc.replace(key, value)
        return doc
        
    def _md_to_html(self, content) -> str:
        # Convert Markdown into HTML; Markdown inside HTML block tags allowed
        html = markdown(content, extensions=['md_in_html'])
        return html
    
    def _generate_from_md(self, page) -> str:
        metadata, content = self._parse_page(page)
        html_content = self._md_to_html(content)
        
        # Get page template from user configuration path
        template = metadata.get("template")
        html_doc = self._config.templates.find(template)

        defaults = self._config.defaults.substitute(metadata)  # Populate tags with user defaults
        modules = self._config.modules.addt({'content':html_content})
        tokens = self._config.tokens.addt(defaults)  # Store page-level template tags
        category = tokens.get("{category}", "")
        active = {f"{{{category}}}":""}

        # Populate "module" subsections before tokens
        html_doc = self._replace_tags(html_doc, modules)
        # Populate tokens in template buffer
        html_doc = self._replace_tags(html_doc, tokens)
        # Activate menu button if applicable
        html_doc = self._replace_tags(html_doc, active)

        # Prettify HTML (compile option)
        if self._config.ispretty:
            try:
                html_doc = indent(html_doc)
            except:
                print("Warning: Page could not be indented")
       
        # Determine final path of new page
        build_dir = self._config.paths.get("build")
        page_name = Path(page).stem  # Filename w/o extension

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
        # TODO: Implement direct HTML file handling
        html_doc: str
        return html_doc
    
    # ****************
    # Public methods
    # ****************
    def generate(self, page) -> None:      
        print(f'Generate: "{page.stem}" page')

        # Handle input file type
        match page.suffix:
            case ".md":
                self._generate_from_md(page)
            case ".html":
                self._generate_from_html(page)
            case _:
                print("Invalid page")
                return