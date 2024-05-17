import json
from os import environ

from main import SubstackClient, send_magic_link


from dotenv import load_dotenv
load_dotenv()
sessionID = environ.get("SUBSTACK_SESSION_ID")
userId = environ.get("SUBSTACK_USER_ID")
substackName = environ.get("SUBSTACK_NAME")
email = environ.get("SUBSTACK_EMAIL")
password = environ.get("SUBSTACK_PASSWORD")
magic_link = environ.get("SUBSTACK_MAGIC_LINK")
if not password and not magic_link:
    send_magic_link(email)
    magic_link = input("Enter magic link: ")

client = SubstackClient(substackName, userId, email, password, magic_link, sessionID)
draft_title = input("Enter title: ")

draft = client.get_draft_by_title(draft_title)

if draft:
    doc = json.loads(draft.get("draft_body"))
    json.dump(doc, open(f"json/{draft_title}.json", "w"))

# recursibely get text form this object
# {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "Introduction"}]}
# {"type": "paragraph", "content": [{"type": "text", "text": "In this section of the series, we will be exploring how to send a "}, {"type": "text", "marks": [{"type": "code"}], "text": "POST"}, {"type": "text", "text": " HTTP request in golang. We will understand how to send a basic POST request, create an HTTP request, and parse json, structs into the request body, add headers, etc in the following sections of this post. We will understand how to marshal the golang struct/types into JSON format, send files in the request, and handle form data with examples of each in this article. Let's answer a few questions first."}]}
# extract text
def parse_json(json_object):
    if isinstance(json_object, list):
        return [parse_json(item) for item in json_object]
    elif isinstance(json_object, dict):
        return {key: parse_json(value) for key, value in json_object.items()}
    else:
        return json_object

def convert_to_markdown(json_data):
    try:
        data = json.loads(json_data)
        markdown_text = ""

        for item in data.get('content', []):
            if item.get('type') == 'heading':
                level = min(max(item.get('attrs', {}).get('level', 1), 1), 6)
                markdown_text += f"{'#' * level} {item['content'][0]['text']}\n\n"
            elif item.get('type') == 'paragraph':
                paragraph_text = ""
                for element in item.get('content', []):
                    if element.get('type') == 'text':
                        paragraph_text += element['text']
                    elif element.get('type') == 'text' and 'code' in element.get('marks', []):
                        paragraph_text += f"`{element['text']}`"
                    elif element.get('type') == 'text' and 'strong' in element.get('marks', []):
                        paragraph_text += f"**{element['text']}**"
                    elif element.get('type') == 'text' and 'italic' in element.get('marks', []):
                        paragraph_text += f"*{element['text']}*"
                    elif element.get('type') == 'text' and 'strikethrough' in element.get('marks', []):
                        paragraph_text += f"~~{element['text']}~~"
                    elif element.get('type') == 'link':
                        paragraph_text += f"[{element['text']}]({element['href']})"
                    elif element.get('type') == 'image':
                        paragraph_text += f"![{element['text']}]({element['src']})"
                    elif element.get('type') == 'bullet_list':
                        for list_element in element.get('content', []):
                            paragraph_text += f"- {list_element.get('content', {}).get('text', '')}\n"
                    elif element.get('type') == 'ordered_list':
                        for element in element.get('content', []):
                            order = element.get('attrs', {}).get('order', 1)
                            paragraph_text += f"{order}. {element['content']['text']}\n"
                    elif element.get('type') == 'blockquote':
                        paragraph_text += f"> {element['content'][0]['text']}\n"
                    elif element.get("type") == "code_block":
                        print(element)
                        paragraph_text += "```"
                        for code in element.get("content", []):
                            paragraph_text += code
                        paragraph_text += "```"
                    else:
                        paragraph_text += element['text']
                markdown_text += f"{paragraph_text}\n"
            elif item.get('type') == 'text':
                markdown_text += item['text']
            elif item.get('type') == 'text' and 'code' in item.get('marks', []):
                markdown_text += f"`{item['text']}`"
            elif item.get('type') == 'text' and 'strong' in item.get('marks', []):
                markdown_text += f"**{item['text']}**"
            elif item.get('type') == 'text' and 'italic' in item.get('marks', []):
                markdown_text += f"*{item['text']}*"
            elif item.get('type') == 'text' and 'strikethrough' in item.get('marks', []):
                markdown_text += f"~~{item['text']}~~"
            elif item.get('type') == 'link':
                markdown_text += f"[{item['text']}]({item['href']})"
            elif item.get('type') == 'image':
                markdown_text += f"![{item['text']}]({item['src']})"
            elif item.get('type') == 'bullet_list':
                list_text = parse_json(item.get('content', []))
                markdown_text += f"- {list_text}\n"
            elif item.get('type') == 'ordered_list':
                for item in item.get('content', []):
                    order = item.get('attrs', {}).get('order', 1)
                    markdown_text += f"{order}. {item['content']['text']}\n"
            elif item.get('type') == 'blockquote':
                markdown_text += f"> {item['content'][0]['text']}\n"
            elif item.get("type") == "code_block":
                markdown_text += "```\n"
                for code in item.get("content", []):
                    markdown_text += code.get("text", "")
                markdown_text += "\n```"
            else:
                markdown_text += item['text']
        
        return markdown_text

    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        return ""

with open(f"json/{draft_title}.json", "r") as file:
    json_data = file.read()

with open(f"md/{draft_title}.md", "w") as file:
    file.write(convert_to_markdown(json_data))
