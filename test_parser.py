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
        expected = """
{
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
        """
        self.assertEqual(json.dumps(parsed), json.dumps(json.loads(expected)))

    def test_heading(self):
        md_text = "# Heading 1\nThis is how you add a new paragraph to your post!"
        expected_structure = {
            "type": "doc",
            "content": [
                {"type": "heading", "attrs": {"level": 1}, "content": [{"type": "text", "text": "Heading 1"}]},
                {"type": "paragraph", "content": [{"type": "text", "text": "This is how you add a new paragraph to your post!"}]}
            ]
        }
        parser = MarkdownConverter()
        parser.parse_markdown(md_text)
        self.assertDictEqual(parser.convert(), expected_structure)

    def test_list(self):
        md_text = "- List item 1\n- List item 2\n- List item 3"
        expected_structure = {
            "type": "doc",
            "content": [
                {"type": "bullet_list", "content": [
                    {"type": "list_item", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "List item 1"}]}]},
                    {"type": "list_item", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "List item 2"}]}]},
                    {"type": "list_item", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "List item 3"}]}]}
                ]}
            ]
        }
        parser = MarkdownConverter()
        parser.parse_markdown(md_text)
        self.assertDictEqual(parser.convert(), expected_structure)

    def test_heading_with_list(self):
        md_text = "## Heading 2\n- List item 1\n- List item 2\n- List item 3"
        expected_structure = {
            "type": "doc",
            "content": [
                {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "Heading 2"}]},
                {"type": "bullet_list", "content": [
                    {"type": "list_item", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "List item 1"}]}]},
                    {"type": "list_item", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "List item 2"}]}]},
                    {"type": "list_item", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "List item 3"}]}]}
                ]}
            ]
        }
        parser = MarkdownConverter()
        parser.parse_markdown(md_text)
        self.assertDictEqual(parser.convert(), expected_structure)



if __name__ == '__main__':
    unittest.main()
