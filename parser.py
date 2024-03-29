import re
import json

def parse_markdown(md_text):
    paragraphs = []

    # Regular expressions for detecting markdown patterns
    heading_pattern = re.compile(r'^(#+)\s+(.*)$')
    bold_pattern = re.compile(r'\*\*(.*?)\*\*')
    italic_pattern = re.compile(r'_(.*?)_')
    strikethrough_pattern = re.compile(r'~~(.*?)~~')
    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    img_pattern = re.compile(r'!\[.*?\]\((.*?)\)')
    unordered_list_pattern = re.compile(r'^\s*-\s+(.*)$')
    ordered_list_pattern = re.compile(r'^\s*\d+\.\s+(.*)$')
    code_block_pattern = re.compile(r'^```.*?$(.*?)^```', re.MULTILINE | re.DOTALL)
    blockquote_pattern = re.compile(r'^>\s+(.*)$')
    horizontal_rule_pattern = re.compile(r'^[-*_]{3,}$')

    # Helper function to convert markdown content into desired structure
    def convert_content(content):
        marks = []
        while bold_pattern.search(content):
            match = bold_pattern.search(content)
            bold_text = match.group(1)
            marks.append({'type': 'strong', 'content': bold_text})
            content = content[:match.start()] + content[match.end():]
        while italic_pattern.search(content):
            match = italic_pattern.search(content)
            italic_text = match.group(1)
            marks.append({'type': 'italic', 'content': italic_text})
            content = content[:match.start()] + content[match.end():]
        while strikethrough_pattern.search(content):
            match = strikethrough_pattern.search(content)
            strikethrough_text = match.group(1)
            marks.append({'type': 'strikethrough', 'content': strikethrough_text})
            content = content[:match.start()] + content[match.end():]
        return {'content': content, 'marks': marks}

    # Helper function to add paragraph to result list
    def add_paragraph(content):
        paragraphs.append({'type': 'paragraph', 'content': content})

    # Iterate through each line in the markdown text
    for line in md_text.splitlines():
        line = line.strip()

        # Handle headings
        if heading_pattern.match(line):
            match = heading_pattern.match(line)
            level = min(len(match.group(1)), 6)  # Maximum heading level is 6
            content = match.group(2)
            paragraphs.append({'type': 'heading', 'level': level, 'content': content})
        # Handle bold, italic, and strikethrough text
        elif bold_pattern.search(line) or italic_pattern.search(line) or strikethrough_pattern.search(line):
            paragraphs.append({'type': 'paragraph', 'content': [convert_content(line)]})
        # Handle links
        elif link_pattern.search(line):
            matches = link_pattern.findall(line)
            for text, href in matches:
                paragraphs.append({'type': 'paragraph', 'content': [convert_content(text)], 'marks': [{'type': 'link', 'href': href}]})
        # Handle images
        elif img_pattern.search(line):
            matches = img_pattern.findall(line)
            for src in matches:
                paragraphs.append({'type': 'captionedImage', 'src': src})
        # Handle unordered lists
        elif unordered_list_pattern.match(line):
            match = unordered_list_pattern.match(line)
            content = match.group(1)
            paragraphs.append({'type': 'list', 'style': 'unordered', 'content': [{'type': 'listItem', 'content': [convert_content(content)]}]})
        # Handle ordered lists
        elif ordered_list_pattern.match(line):
            match = ordered_list_pattern.match(line)
            content = match.group(1)
            paragraphs.append({'type': 'list', 'style': 'ordered', 'content': [{'type': 'listItem', 'content': [convert_content(content)]}]})
        # Handle code blocks
        elif line.startswith("```"):
            match = code_block_pattern.search(md_text)
            if match:
                code_block_content = match.group(1).strip()
                paragraphs.append({'type': 'codeBlock', 'content': code_block_content})
        # Handle blockquotes
        elif blockquote_pattern.match(line):
            match = blockquote_pattern.match(line)
            content = match.group(1)
            paragraphs.append({'type': 'blockquote', 'content': [convert_content(content)]})
        # Handle horizontal rules
        elif horizontal_rule_pattern.match(line):
            paragraphs.append({'type': 'horizontalRule'})
        # Handle regular paragraphs
        else:
            if line:
                add_paragraph([convert_content(line)])

    return paragraphs

# Example usage
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

* Unordered list item 1
* Unordered list item 2

1. Ordered list item 1
2. Ordered list item 2
print("This is a code block")

yaml
Copy code

> This is a blockquote

---

This is a regular paragraph with some **bold**, _italic_, and ~~strikethrough~~ text.
"""
parsed_structure = parse_markdown(md_text)
print(json.dumps(parsed_structure, indent=2))
with open("output.json", "w") as file:
    json.dump(parsed_structure, file, indent=4)

