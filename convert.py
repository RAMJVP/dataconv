import re
from lxml import etree


def parse_latex(file_path):
    """
    Parse the LaTeX file and extract structured content.
    Args:
        file_path (str): Path to the LaTeX file.
    Returns:
        dict: Parsed content as a dictionary.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        latex_content = file.read()
    
    # Extract key elements using regular expressions
    parsed_content = {
        "title": re.search(r"\\title\{(.+?)\}", latex_content).group(1) if re.search(r"\\title\{(.+?)\}", latex_content) else None,
        "authors": re.findall(r"\\author\{(.+?)\}", latex_content),
        "abstract": re.search(r"\\begin\{abstract\}(.+?)\\end\{abstract\}", latex_content, re.DOTALL).group(1).strip() if re.search(r"\\begin\{abstract\}(.+?)\\end\{abstract\}", latex_content, re.DOTALL) else None,
        "sections": re.findall(r"\\section\{(.+?)\}", latex_content),
        "subsections": re.findall(r"\\subsection\{(.+?)\}", latex_content),
    }
    
    return parsed_content

# Test the parsing function
if __name__ == "__main__":
    latex_file = "main.tex"
    content = parse_latex(latex_file)
    print("Parsed LaTeX Content:")
    print(content)







def generate_xml(parsed_content, output_file):
    """
    Generate an XML file from parsed LaTeX content.
    Args:
        parsed_content (dict): Parsed LaTeX content.
        output_file (str): Path to save the generated XML file.
    """
    # Create root element
    root = etree.Element("article", attrib={"article-type": "research-article", "dtd-version": "1.2"})
    front = etree.SubElement(root, "front")

    # Add title
    title_group = etree.SubElement(front, "title-group")
    article_title = etree.SubElement(title_group, "article-title")
    article_title.text = parsed_content.get("title", "No Title Provided")
    
    # Add authors
    contrib_group = etree.SubElement(front, "contrib-group")
    for author in parsed_content.get("authors", []):
        contrib = etree.SubElement(contrib_group, "contrib", attrib={"contrib-type": "author"})
        string_name = etree.SubElement(contrib, "string-name")
        string_name.text = author

    # Add abstract
    abstract = etree.SubElement(front, "abstract")
    abstract.text = parsed_content.get("abstract", "No Abstract Provided")
    
    # Add sections
    body = etree.SubElement(root, "body")
    for section in parsed_content.get("sections", []):
        sec = etree.SubElement(body, "sec")
        title = etree.SubElement(sec, "title")
        title.text = section
    
    # Write XML to file
    tree = etree.ElementTree(root)
    tree.write(output_file, pretty_print=True, xml_declaration=True, encoding="UTF-8")
    print(f"XML file generated at {output_file}")

# Test the XML generation
if __name__ == "__main__":
    latex_file = "main.tex"
    output_xml = "output.xml"

    # Parse LaTeX and generate XML
    content = parse_latex(latex_file)
    generate_xml(content, output_xml)
