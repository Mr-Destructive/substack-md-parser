import unittest
from parser import MarkdownConverter


class TestSubstackParser(unittest.TestCase):
    maxDiff = None

    def test_substack_md_parser(self):

        import parser
        import json

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
        parsed = parser.convert()
        expected_structure = {
          "type": "doc",
          "content": [
            {
              "type": "heading",
              "attrs": {
                "level": 1
              },
              "content": [
                {
                  "type": "text",
                  "text": "Heading 1"
                }
              ]
            },
            {
              "type": "paragraph",
              "content": [
                {
                  "type": "text",
                  "text": "This is how you add a new paragraph to your post!"
                }
              ]
            },
            {
              "type": "ordered_list",
              "attrs": {
                "start": 1,
                "order": 1
              },
              "content": [
                {
                  "type": "list_item",
                  "content": [
                    {
                      "type": "paragraph",
                      "content": [
                        {
                          "type": "text",
                          "text": "List item 1"
                        }
                      ]
                    }
                  ]
                },
                {
                  "type": "list_item",
                  "content": [
                    {
                      "type": "paragraph",
                      "content": [
                        {
                          "type": "text",
                          "text": "List item 2"
                        }
                      ]
                    }
                  ]
                },
                {
                  "type": "list_item",
                  "content": [
                    {
                      "type": "paragraph",
                      "content": [
                        {
                          "type": "text",
                          "text": "List item 3"
                        }
                      ]
                    }
                  ]
                }
              ]
            },
            {
                "type": "paragraph",
                "content": []
            },
            {
              "type": "heading",
              "attrs": {
                "level": 2
              },
              "content": [
                {
                  "type": "text",
                  "text": "Heading 2"
                }
              ]
            },
            {
              "type": "paragraph",
              "content": [
                {
                  "type": "text",
                  "text": "This is how you add a new paragraph to your post!"
                }
              ]
            }
          ]
}

        self.assertDictEqual(parsed, expected_structure)

    def test_heading(self):
        md_text = "# Heading 1\nThis is how you add a new paragraph to your post!"
        expected_structure = {
            "type": "doc",
            "content": [
                {
                    "type": "heading",
                    "attrs": {"level": 1},
                    "content": [{"type": "text", "text": "Heading 1"}],
                },
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": "This is how you add a new paragraph to your post!",
                        }
                    ],
                },
            ],
        }
        parser = MarkdownConverter()
        parser.parse_markdown(md_text)
        print(parser.convert(), expected_structure)
        self.assertDictEqual(parser.convert(), expected_structure)

    def test_list(self):
        md_text = "- List item 1\n- List item 2\n- List item 3"
        expected_structure = {
            "type": "doc",
            "content": [
                {
                    "type": "bullet_list",
                    "content": [
                        {
                            "type": "list_item",
                            "content": [
                                {
                                    "type": "paragraph",
                                    "content": [
                                        {"type": "text", "text": "List item 1"}
                                    ],
                                }
                            ],
                        },
                        {
                            "type": "list_item",
                            "content": [
                                {
                                    "type": "paragraph",
                                    "content": [
                                        {"type": "text", "text": "List item 2"}
                                    ],
                                }
                            ],
                        },
                        {
                            "type": "list_item",
                            "content": [
                                {
                                    "type": "paragraph",
                                    "content": [
                                        {"type": "text", "text": "List item 3"}
                                    ],
                                }
                            ],
                        },
                    ],
                }
            ],
        }
        parser = MarkdownConverter()
        parser.parse_markdown(md_text)
        self.assertDictEqual(parser.convert(), expected_structure)

    def test_heading_with_list(self):
        md_text = "## Heading 2\n- List item 1\n- List item 2\n- List item 3"
        expected_structure = {
            "type": "doc",
            "content": [
                {
                    "type": "heading",
                    "attrs": {"level": 2},
                    "content": [{"type": "text", "text": "Heading 2"}],
                },
                {
                    "type": "bullet_list",
                    "content": [
                        {
                            "type": "list_item",
                            "content": [
                                {
                                    "type": "paragraph",
                                    "content": [
                                        {"type": "text", "text": "List item 1"}
                                    ],
                                }
                            ],
                        },
                        {
                            "type": "list_item",
                            "content": [
                                {
                                    "type": "paragraph",
                                    "content": [
                                        {"type": "text", "text": "List item 2"}
                                    ],
                                }
                            ],
                        },
                        {
                            "type": "list_item",
                            "content": [
                                {
                                    "type": "paragraph",
                                    "content": [
                                        {"type": "text", "text": "List item 3"}
                                    ],
                                }
                            ],
                        },
                    ],
                },
            ],
        }
        parser = MarkdownConverter()
        parser.parse_markdown(md_text)
        self.assertDictEqual(parser.convert(), expected_structure)

    def test_link(self):
        md_text = "[View Link](https://whoraised.substack.com/)"
        expected_structure = {
            "type": "doc",
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "marks": [
                                {
                                    "type": "link",
                                    "attrs": {
                                        "href": "https://whoraised.substack.com/",
                                        "target": "_blank",
                                        "rel": "noopener noreferrer nofollow",
                                        "class": None,
                                    },
                                }
                            ],
                            "text": "View Link",
                        }
                    ],
                }
            ],
        }
        parser = MarkdownConverter()
        parser.parse_markdown(md_text)
        self.assertDictEqual(parser.convert(), expected_structure)

    def test_multiple_links(self):
        md_text = """
# Hello
[View Link 1](https://whoraised.substack.com/)

Below is a link
[View Link 2](https://whoraised.substack.com/)

[View Link 3](https://whoraised.substack.com/)
        """

        expected_structure = {
            "type": "doc",
            "content": [
                {
                    "type": "heading",
                    "attrs": {"level": 1},
                    "content": [{"type": "text", "text": "Hello"}],
                },
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "marks": [
                                {
                                    "type": "link",
                                    "attrs": {
                                        "href": "https://whoraised.substack.com/",
                                        "target": "_blank",
                                        "rel": "noopener noreferrer nofollow",
                                        "class": None,
                                    },
                                }
                            ],
                            "text": "View Link 1",
                        }
                    ],
                },
                {"type": "paragraph", "content": []},
                {
                    "type": "paragraph",
                    "content": [{"type": "text", "text": "Below is a link"}],
                },
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "marks": [
                                {
                                    "type": "link",
                                    "attrs": {
                                        "href": "https://whoraised.substack.com/",
                                        "target": "_blank",
                                        "rel": "noopener noreferrer nofollow",
                                        "class": None,
                                    },
                                }
                            ],
                            "text": "View Link 2",
                        }
                    ],
                },
                {"type": "paragraph", "content": []},
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "marks": [
                                {
                                    "type": "link",
                                    "attrs": {
                                        "href": "https://whoraised.substack.com/",
                                        "target": "_blank",
                                        "rel": "noopener noreferrer nofollow",
                                        "class": None,
                                    },
                                }
                            ],
                            "text": "View Link 3",
                        }
                    ],
                },
            ],
        }
        parser = MarkdownConverter()
        parser.parse_markdown(md_text)
        self.assertDictEqual(parser.convert(), expected_structure)

    def test_bolden_text(self):
        md_text = "This is how you **bolden** a word."
        expected_structure = {
            "type": "doc",
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {"type": "text", "text": "This is how you "},
                        {
                            "type": "text",
                            "marks": [
                                {
                                    "type": "strong",
                                }
                            ],
                            "text": "bolden",
                        },
                        {"type": "text", "text": " a word."},
                    ],
                }
            ],
        }
        parser = MarkdownConverter()
        parser.parse_markdown(md_text)
        self.assertDictEqual(parser.convert(), expected_structure)

    def test_italic_text(self):
        md_text = "This is how you *italic* a word."
        expected_structure = {
            "type": "doc",
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {"type": "text", "text": "This is how you "},
                        {
                            "type": "text",
                            "marks": [
                                {
                                    "type": "italic",
                                }
                            ],
                            "text": "italic",
                        },
                        {"type": "text", "text": " a word."},
                    ],
                }
            ],
        }
        parser = MarkdownConverter()
        parser.parse_markdown(md_text)
        self.assertDictEqual(parser.convert(), expected_structure)

    def test_strikethrough_text(self):
        md_text = "This is how you ~~strikethrough~~ a word."
        expected_structure = {
            "type": "doc",
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {"type": "text", "text": "This is how you "},
                        {
                            "type": "text",
                            "marks": [
                                {
                                    "type": "strikethrough",
                                }
                            ],
                            "text": "strikethrough",
                        },
                        {"type": "text", "text": " a word."},
                    ],
                }
            ],
        }
        parser = MarkdownConverter()
        parser.parse_markdown(md_text)
        self.assertDictEqual(parser.convert(), expected_structure)

    def test_bold_italics(self):
        md_text = "This is how you *italic* and **bold** a word."
        expected_structure = {
            "type": "doc",
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {"type": "text", "text": "This is how you "},
                        {
                            "type": "text",
                            "marks": [
                                {
                                    "type": "italic",
                                }
                            ],
                            "text": "italic",
                        },
                        {"type": "text", "text": " and "},
                        {
                            "type": "text",
                            "marks": [
                                {
                                    "type": "strong",
                                }
                            ],
                            "text": "bold",
                        },
                        {"type": "text", "text": " a word."},
                    ],
                }
            ],
        }
        parser = MarkdownConverter()
        parser.parse_markdown(md_text)
        self.assertDictEqual(parser.convert(), expected_structure)

    def test_code(self):
        md_text = """
This is a `code` highlighted.
nothing.
Some more `code goes here` and `there`
        """
        expected_structure = {
            "type": "doc",
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {"type": "text", "text": "This is a "},
                        {"type": "text", "marks": [{"type": "code"}], "text": "code"},
                        {"type": "text", "text": " highlighted."},
                    ],
                },
                {"type": "paragraph", "content": [{"type": "text", "text": "nothing."}]},
                {
                    "type": "paragraph",
                    "content": [
                        {"type": "text", "text": "Some more "},
                        {"type": "text", "marks": [{"type": "code"}], "text": "code goes here"},
                        {"type": "text", "text": " and "},
                        {"type": "text", "marks": [{"type": "code"}], "text": "there"},
                    ],
                },
            ],
        }
        parser = MarkdownConverter()
        parser.parse_markdown(md_text)
        self.assertDictEqual(parser.convert(), expected_structure)

    def test_link_list(self):
        md_text = """
        - This is a link [View 1](https://whoraised.substack.com/)
        - [View 2](https://whoraised.substack.com/)
        - [View 3](https://whoraised.substack.com/)
        """
        expected_structure ={
            "type": "doc",
            "content": [
                {
                    "type": "bullet_list",
                    "content": [
                        {
                            "type": "list_item",
                            "content": [
                                {
                                    "type": "paragraph",
                                    "content": [
                                        {
                                            "type": "text",
                                            "content": "This is a link ",

                                        },
                                        {
                                            "type": "text",
                                            "marks": [
                                                {
                                                    "type": "link",
                                                    "attrs": {
                                                        "href": "https://whoraised.substack.com/",
                                                        "target": "_blank",
                                                        "rel": "noopener noreferrer nofollow",
                                                        "class": None,
                                                    },
                                                }
                                            ],
                                            "text": "View 1",
                                        }
                                    ],
                                }
                            ],
                        },
                        {
                            "type": "list_item",
                            "content": [
                                {
                                    "type": "paragraph",
                                    "content": [
                                        {
                                            "type": "text",
                                            "marks": [
                                                {
                                                    "type": "link",
                                                    "attrs": {
                                                        "href": "https://whoraised.substack.com/",
                                                        "target": "_blank",
                                                        "rel": "noopener noreferrer nofollow",
                                                        "class": None,
                                                    },
                                                }
                                            ],
                                            "text": "View 2",
                                        }
                                    ],
                                }
                            ],
                        },
                        {
                            "type": "list_item",
                            "content": [
                                {
                                    "type": "paragraph",
                                    "content": [
                                        {
                                            "type": "text",
                                            "marks": [
                                                {
                                                    "type": "link",
                                                    "attrs": {
                                                        "href": "https://whoraised.substack.com/",
                                                        "target": "_blank",
                                                        "rel": "noopener noreferrer nofollow",
                                                        "class": None,
                                                    },
                                                }
                                            ],
                                            "text": "View 3",
                                        }
                                    ],
                                }
                            ],
                        },
                    ],
                },
            ],
        }


if __name__ == "__main__":
    unittest.main()
