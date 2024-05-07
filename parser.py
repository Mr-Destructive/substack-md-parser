import json
import re


class MarkdownConverter:
    def __init__(self):
        self.draft_body = {"type": "doc", "content": []}
        # Regular expressions for detecting markdown patterns
        self.heading_pattern = re.compile(r"^(#+)\s+(.*)$")
        self.unordered_list_pattern = re.compile(
            r"^\s*[-*+]\s+(.*)$"
        )  # Pattern for unordered list items
        self.ordered_list_pattern = re.compile(
            r"^\s*(\d+\.)\s+(.*)$"
        )  # Pattern for ordered list items
        self.link_pattern = re.compile(r"\[(.*?)\]\((.*?)\)")  # Pattern for links
        self.bold_pattern = re.compile(r"\*\*(.*?)\*\*")  # Pattern for bold text
        self.italic_pattern = re.compile(r"\*(.*?)\*")  # Pattern for italic text
        self.strike_pattern = re.compile(r"~~(.*?)~~")  # Pattern for strikethrough text
        self.blockquote_pattern = re.compile(r"> (.*?)$")  # Pattern for quote
        self.open_tags = []
        self.current_text = ""

    def parse_markdown(self, md_text):
        # Split markdown text into lines
        lines = md_text.strip().split("\n")

        current_list = None

        for line in lines:
            line = line.strip()

            if self.heading_pattern.match(line):
                match = self.heading_pattern.match(line)
                level = min(len(match.group(1)), 6)  # Maximum heading level is 6
                content = match.group(2)
                self.add_heading(content, level)
            elif self.unordered_list_pattern.match(line):
                if current_list is None:
                    current_list = {"type": "bullet_list", "content": []}
                list_item = self.unordered_list_pattern.match(line).group(1).strip()
                current_list["content"].append(
                    {
                        "type": "list_item",
                        "content": [
                            {
                                "type": "paragraph",
                                "content": [{"type": "text", "text": list_item}],
                            }
                        ],
                    }
                )
            elif self.ordered_list_pattern.match(line):
                if current_list is None or current_list["type"] != "ordered_list":
                    # Start a new ordered list
                    current_list = {
                        "type": "ordered_list",
                        "attrs": {
                            "start": 1,
                            "order": 1
                        },
                        "content": []
                    }

                list_item = self.ordered_list_pattern.match(line).group(2).strip()
                current_list["content"].append(
                    {
                        "type": "list_item",
                        "content": [
                            {
                                "type": "paragraph",
                                "content": [{"type": "text", "text": list_item}]},
                        ],
                    }
                )
            elif self.link_pattern.search(line):
                match = self.link_pattern.search(line)
                link_text = match.group(1)
                link_url = match.group(2)
                text_before_link = line[: match.start()]
                text_after_link = line[match.end() :]
                link_content = self.add_link(link_text, link_url)
                if text_before_link and text_after_link:
                    self.draft_body["content"].append(
                        {
                            "type": "paragraph",
                            "content": [
                                {"type": "text", "text": text_before_link},
                                link_content,
                                {"type": "text", "text": text_after_link},
                            ],
                        }
                    )
                elif text_before_link:
                    self.draft_body["content"].append(
                        {
                            "type": "paragraph",
                            "content": [
                                {"type": "text", "text": text_before_link},
                                link_content,
                            ],
                        }
                    )
                elif text_after_link:
                    self.draft_body["content"].append(
                        {
                            "type": "paragraph",
                            "content": [
                                link_content,
                                {"type": "text", "text": text_after_link},
                            ],
                        }
                    )
                else:
                    self.draft_body["content"].append(
                        {
                            "type": "paragraph",
                            "content": [
                                link_content,
                            ],
                        }
                    )
            elif self.blockquote_pattern.match(line):
                match = self.blockquote_pattern.match(line)
                content = match.group(1)
                self.draft_body["content"].append(
                    {"type": "blockquote", "content": [{"type": "paragraph", "content": [{"type": "text", "text": content}]}]}
                )
            else:
                content = self.handle_inline_formatting(line)
                if content:
                    self.draft_body["content"].append({"type": "paragraph", "content": content})
                # Add any remaining text
                # self.current_text += line
                if line:
                    pass
                    # self.add_text(line)
                if not content and current_list:
                    self.draft_body["content"].append(current_list)
                    current_list = None

        #if current_list:
            #self.draft_body["content"].append(current_list)

    def add_text(self, text, mark=None):
        content = [{"type": "text", "text": text}]
        if mark:
            content[0]["marks"] = [{"type": mark}]
        self.draft_body["content"].append({"type": "paragraph", "content": content})

    def add_paragraph(self, content):
        self.draft_body["content"].append(
            {"type": "paragraph", "content": [{"type": "text", "text": content}]}
        )

    def add_heading(self, content, level=1):
        self.draft_body["content"].append(
            {
                "type": "heading",
                "attrs": {"level": level},
                "content": [{"type": "text", "text": content}],
            }
        )

    def add_bullet_list(self, items):
        list_content = [
            {
                "type": "list_item",
                "content": [
                    {"type": "paragraph", "content": [{"type": "text", "text": item}]}
                ],
            }
            for item in items
        ]
        self.draft_body["content"].append(
            {"type": "bullet_list", "content": list_content}
        )

    def add_link(self, link_text, link_url):
        link_node = {
            "type": "text",
            "marks": [
                {
                    "type": "link",
                    "attrs": {
                        "href": link_url,
                        "target": "_blank",
                        "rel": "noopener noreferrer nofollow",
                        "class": None,
                    },
                }
            ],
            "text": link_text,
        }
        return link_node

    def add_bold_text(self, line):
        bold_matches = re.finditer(r"\*\*(.*?)\*\*", line)
        bold_content = []
        start_index = 0
        for match in bold_matches:
            if match.start() > start_index:
                bold_content.append(
                    {"type": "text", "text": line[start_index : match.start()]}
                )
            bold_content.append(
                {"type": "text", "marks": [{"type": "strong"}], "text": match.group(1)}
            )
            start_index = match.end()
        if start_index < len(line):
            bold_content.append({"type": "text", "text": line[start_index:]})
        self.draft_body["content"].append(
            {"type": "paragraph", "content": bold_content}
        )

    def add_italic_text(self, line):
        italic_matches = re.finditer(r"\*(.*?)\*", line)
        italic_content = []
        start_index = 0
        for match in italic_matches:
            if match.start() > start_index:
                italic_content.append(
                    {"type": "text", "text": line[start_index : match.start()]}
                )
            italic_content.append(
                {"type": "text", "marks": [{"type": "italic"}], "text": match.group(1)}
            )
            start_index = match.end()
        if start_index < len(line):
            italic_content.append({"type": "text", "text": line[start_index:]})
        self.draft_body["content"].append(
            {"type": "paragraph", "content": italic_content}
        )

    def add_strikethrough_text(self, line):
        strikethrough_matches = re.finditer(r"~~(.*?)~~", line)
        strikethrough_content = []
        start_index = 0
        for match in strikethrough_matches:
            if match.start() > start_index:
                strikethrough_content.append(
                    {"type": "text", "text": line[start_index : match.start()]}
                )
            strikethrough_content.append(
                {
                    "type": "text",
                    "marks": [{"type": "strikethrough"}],
                    "text": match.group(1),
                }
            )
            start_index = match.end()
        if start_index < len(line):
            strikethrough_content.append({"type": "text", "text": line[start_index:]})
        self.draft_body["content"].append(
            {"type": "paragraph", "content": strikethrough_content}
        )

    def handle_inline_formatting(self, line):
        start_index = 0
        content = []

        while True:
            match = re.search(r"\*\*(.*?)\*\*|\*(.*?)\*|~~(.*?)~~", line[start_index:])
            if not match:
                break

            match_start = match.start() + start_index
            match_end = match.end() + start_index
            tag = match.group(1) or match.group(2) or match.group(3)

            # Add text before the match
            if match_start > start_index:
                content.append({"type": "text", "text": line[start_index:match_start]})

            # Process the matched inline formatting
            if match.group(1):
                content.append(
                    {"type": "text", "marks": [{"type": "strong"}], "text": tag}
                )
            elif match.group(2):
                content.append(
                    {"type": "text", "marks": [{"type": "italic"}], "text": tag}
                )
            elif match.group(3):
                content.append(
                    {"type": "text", "marks": [{"type": "strikethrough"}], "text": tag}
                )

            # Update the start index for the next iteration
            start_index = match_end

        # Add remaining text after processing all matches
        if start_index < len(line):
            content.append({"type": "text", "text": line[start_index:]})

        # Add the paragraph node to the draft body
        return content

    def convert(self):
        return self.draft_body


# Example usage
# md_text = """
## Heading 1
# - List item
# - List item
# - List item
#
### Heading 2
#### Heading 3
#
# This is how you add a new paragraph to your post!
#
# This is how you **bolden** a word.
#
# [View Link](https://whoraised.substack.com/)
#
# * Unordered list item 1
# * Unordered list item 2
#
# 1. Ordered list item 1
# 2. Ordered list item 2
# print("This is a code block")
#
# yaml
# Copy code
#
# > This is a blockquote
#
# ---
#
# This is a regular paragraph with some **bold**, _italic_, and ~~strikethrough~~ text.
# """
md_text = """
# Heading 1
This is how you add a new paragraph to your post!
1. List item 1
2. List item 2
3. List item 3
This is a link [here](https://www.meetgor.com).

This is some **bolden** text.

## Heading 2
This is how you add a new paragraph to your post!
"""

md_text_heading = """
# Hello, World!
"""

md_text_o_lists = """
1. List item 1
2. List item 2
3. List item 3
"""

md_text_uno_lists = """
- List item 1
- List item 2
- List item 3
"""

md_text_link = """
This is a link [here](https://www.meetgor.com).
"""

md_text_link = "[View Link](https://whoraised.substack.com/)"
md_text_multiple_links = """
# Hello
[View Link 1](https://whoraised.substack.com/)

Below is a link
[View Link 2](https://whoraised.substack.com/)

[View Link 3](https://whoraised.substack.com/)
"""

md_text_bold = """
This is how you **bolden** a word.
"""

md_text_italic = """
This is how you *italic* a word.
"""
md_text_bolic = """
This is how you *italic* and **bold** a word and ~~this~~ is a link [here](https://www.meetgor.com). 
"""

md_text_nested_bolic = """
This is ~~cut badly~~ **~~and boldy~~** 
"""

md_text = """
# Heading 1
This is how you add a new paragraph to your post!
1. List item 1
2. List item 2
3. List item 3

## Heading 2
This is how you add a new paragraph to your post!
"""

md_text_quote = """
> This is a blockquote
"""


parser = MarkdownConverter()
parser.parse_markdown(md_text_quote)
parsed_structure = parser.convert()

print(parsed_structure)
with open("output.json", "w") as file:
    json.dump(parsed_structure, file, indent=4)

expected_dict = json.loads(open("expected_output.json").read())
expected_output = expected_dict["blockquote"]
print(expected_output)

assert parsed_structure == expected_output

md_text = "This is ~~cut badly~~ **~~and boldy~~**"
