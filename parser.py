import json

def parse_markdown(md_text):
    paragraphs = []
    current_paragraph = ""
    in_paragraph = False

    for line in md_text.splitlines():
        if line.strip() == "":
            if in_paragraph:
                paragraphs.append({"type": "paragraph", "content": [{"type": "text", "text": current_paragraph.strip()}]})
                current_paragraph = ""
                in_paragraph = False
        elif line.startswith("#"):
            if in_paragraph:
                paragraphs.append({"type": "paragraph", "content": [{"type": "text", "text": current_paragraph.strip()}]})
                current_paragraph = ""
                in_paragraph = False

            heading_level = len(line.split()[0])
            heading_content = line.strip("# ").strip()
            paragraphs.append({"type": "heading", "level": heading_level, "content": heading_content})
        elif line.startswith(">"):
            if in_paragraph:
                paragraphs.append({"type": "paragraph", "content": [{"type": "text", "text": current_paragraph.strip()}]})
                current_paragraph = ""
                in_paragraph = False

            quote = line.strip()[1:].strip()
            paragraphs.append({"type": "quote", "content": quote})
        elif line.startswith("**") and line.endswith("**"):
            if in_paragraph:
                paragraphs.append({"type": "paragraph", "content": [{"type": "text", "text": current_paragraph.strip()}]})
                current_paragraph = ""
                in_paragraph = False

            bold_parts = line.split("**")
            bold_content = []
            for i in range(1, len(bold_parts), 2):
                bold_content.append({"type": "text", "text": bold_parts[i]})
            paragraphs.append({"type": "paragraph", "content": bold_content})
        elif "[" in line and "]" in line and "(" in line and ")" in line:
            if in_paragraph:
                paragraphs.append({"type": "paragraph", "content": [{"type": "text", "text": current_paragraph.strip()}]})
                current_paragraph = ""
                in_paragraph = False

            link_start = line.index("[")
            link_end = line.index("]")
            link_text = line[link_start + 1:link_end]
            href_start = line.index("(")
            href_end = line.index(")")
            href_text = line[href_start + 1:href_end]
            paragraphs.append({"type": "paragraph", "content": [{"type": "link", "href": href_text, "text": link_text}]})
        elif line.startswith("![") and line.endswith(")"):
            if in_paragraph:
                paragraphs.append({"type": "paragraph", "content": [{"type": "text", "text": current_paragraph.strip()}]})
                current_paragraph = ""
                in_paragraph = False

            img_parts = line.split("](")
            src = img_parts[1][:-1]
            paragraphs.append({"type": "captionedImage", "src": src})
        else:
            if not in_paragraph:
                in_paragraph = True

            current_paragraph += " " + line.strip()

    if current_paragraph:
        paragraphs.append({"type": "paragraph", "content": [{"type": "text", "text": current_paragraph.strip()}]})
        
    # Escaping braces in the content
    for paragraph in paragraphs:
        if paragraph["type"] == "paragraph":
            for content_item in paragraph["content"]:
                if content_item["type"] == "text":
                    content_item["text"] = content_item["text"].replace('"', '\"').replace("{", "\\{").replace("}", "\\}")

    return paragraphs


if __name__ == "__main__":
    with open("temp.md", "r") as file:
        md_text = file.read()
    md_text = """

    # Heading 1
    - List item
    - List item
    - List item
    
    ## Heading 2
    ### Heading 3

    This is how you add a new paragraph to your post!

    This is how you **bolden** a word.

    [View Link](https://whoraised.substack.com/)

    """

    parsed = parse_markdown(md_text)
    with open("temp.json", "w") as file:
        json.dump(parsed, file)
