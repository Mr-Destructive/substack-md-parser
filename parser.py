import json
import re


class MarkdownConverter:
    def __init__(self):
        self.draft_body = {"type": "doc", "content": []}

    def parse_markdown(self, md_text):
        # Split markdown text into lines
        lines = md_text.strip().split('\n')

        # Regular expressions for detecting markdown patterns
        heading_pattern = re.compile(r'^(#+)\s+(.*)$')
        unordered_list_pattern = re.compile(r'^\s*[-*+]\s+(.*)$')  # Pattern for unordered list items
        ordered_list_pattern = re.compile(r'^\s*(\d+\.)\s+(.*)$')  # Pattern for ordered list items

        current_list = None

        for line in lines:
            line = line.strip()
            if heading_pattern.match(line):
                match = heading_pattern.match(line)
                level = min(len(match.group(1)), 6)  # Maximum heading level is 6
                content = match.group(2)
                self.add_heading(content, level)
            elif unordered_list_pattern.match(line):
                if current_list is None:
                    current_list = {"type": "bullet_list", "content": []}
                list_item = unordered_list_pattern.match(line).group(1).strip()
                current_list["content"].append({"type": "list_item", "content": [{"type": "paragraph", "content": [{"type": "text", "text": list_item}]}]})
            elif ordered_list_pattern.match(line):
                if current_list is None:
                    current_list = {"type": "ordered_list", "attrs": {"start": 1, "order": 1}, "content": []}
                list_item = ordered_list_pattern.match(line).group(2).strip()
                current_list["content"].append({"type": "list_item", "content": [{"type": "paragraph", "content": [{"type": "text", "text": list_item}]}]})
            else:
                if current_list is not None:
                    self.draft_body["content"].append(current_list)
                    current_list = None
                if line:
                    self.add_paragraph(line)

        if current_list is not None:
            self.draft_body["content"].append(current_list)

    def add_paragraph(self, content):
        self.draft_body["content"].append({"type": "paragraph", "content": [{"type": "text", "text": content}]})

    def add_heading(self, content, level=1):
        self.draft_body["content"].append({"type": "heading", "attrs": {"level": level}, "content": [{"type": "text", "text": content}]})

    def add_bullet_list(self, items):
        list_content = [{"type": "list_item", "content": [{"type": "paragraph", "content": [{"type": "text", "text": item}]}]} for item in items]
        self.draft_body["content"].append({"type": "bullet_list", "content": list_content})

    def convert(self):
        return self.draft_body

# Example usage
#md_text = """
## Heading 1
#- List item
#- List item
#- List item
#    
### Heading 2
#### Heading 3
#
#This is how you add a new paragraph to your post!
#
#This is how you **bolden** a word.
#
#[View Link](https://whoraised.substack.com/)
#
#* Unordered list item 1
#* Unordered list item 2
#
#1. Ordered list item 1
#2. Ordered list item 2
#print("This is a code block")
#
#yaml
#Copy code
#
#> This is a blockquote
#
#---
#
#This is a regular paragraph with some **bold**, _italic_, and ~~strikethrough~~ text.
#"""
md_text = """
# Heading 1
This is how you add a new paragraph to your post!
1. List item 1
2. List item 2
3. List item 3

## Heading 2
This is how you add a new paragraph to your post!
"""
parser = MarkdownConverter()
parser.parse_markdown(md_text)
parsed_structure = parser.convert()

print(json.dumps(parsed_structure, indent=2))
with open("output.json", "w") as file:
    json.dump(parsed_structure, file, indent=4)

