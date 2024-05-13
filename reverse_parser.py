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
    print(doc)
    json.dump(doc, open("revtemp.md", "w"))

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
                        paragraph_text += f"- {element['content'][0]['text']}\n"
                    elif element.get('type') == 'ordered_list':
                        paragraph_text += f"{element['content'][0]['text']}\n"
                    elif element.get('type') == 'blockquote':
                        paragraph_text += f"> {element['content'][0]['text']}\n"
                    elif element.get("type") == "code_block":
                        paragraph_text += f"```\n{element['text']}\n```"
                    else:
                        paragraph_text += element['text']
                markdown_text += f"{paragraph_text}\n"
        
        return markdown_text

    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        return ""

with open("revtemp.md", "r") as file:
    json_data = file.read()
    print(convert_to_markdown(json_data))

with open("md/rev.md", "w") as file:
    file.write(convert_to_markdown(json_data))
