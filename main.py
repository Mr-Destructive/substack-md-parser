from os import environ
import os
import markdown
import requests
import json
import tempfile

from parser import MarkdownConverter


class NodeType:
    Paragraph = "paragraph"
    Text = "text"
    Doc = "doc"


class DraftBylines:
    def __init__(self, ID):
        self.id = ID


class Draft:
    def __init__(self, draft_title, draft_body, draft_bylines, audience=None, post_type=None):
        self.draft_title = draft_title
        self.draft_bylines = draft_bylines
        self.draft_body = draft_body

def parse(s):
    html_content = markdown.markdown(s, extensions=['extra'])
    return html_content

def parse_html_to_substack(html_content):
    return html_content
    #return {
    #    "type": NodeType.Doc,
    #    "content": [{
    #        "type": NodeType.Paragraph,
    #        "content": [
    #            {
    #                "type": NodeType.Text,
    #                "text": html_content
    #            }
    #        ]
    #    }]
    #}
def convert_to_substack(md_text):
    #html_content = parse(md_text)
    #substack_post = parse_html_to_substack(html_content)
    substack_parser = MarkdownConverter()
    substack_parser.parse_markdown(md_text)
    contents = substack_parser.convert()
    substack_post = contents
    #substack_post = {
    #    "type": NodeType.Doc,
    #    "content": contents
    #}
    return substack_post

class SubstackClient:
    def __init__(self, substack_name, userId, email, password, magic_link, session_id):
        self.substack_name = substack_name
        self.substack_url = f"https://{self.substack_name}.substack.com"
        self.client = requests.Session()
        self.userId = userId
        auth_response = self.login(email, password, magic_link, session_id)
        cookies = auth_response.cookies
        self.client.cookies = cookies
        self.split_cookies()
        self.session_id = self.cookie_dict.get("substack.sid", "")
        with open("session_id.txt", "w") as file:
            file.write(self.session_id)

    def split_cookies(self):
        self.cookie_dict = {}
        for cookie, value in self.client.cookies.get_dict().items():
            self.cookie_dict[cookie] = value

    def login(self, email, password, magic_link, session_id):
        if session_id:
            self.client = requests.Session()
            self.client.cookies.set("substack.sid", session_id)
            response = self.client
        elif email and password and not magic_link:
            endpoint = f"https://substack.com/api/v1/login"
            payload = {
                "captcha_response": None,
                "email": email,
                "password": password,
                "redirect": "/",
                "for_pub": "",
            }
            response = requests.post(endpoint, json=payload)
        elif magic_link:
            response = requests.get(magic_link)
        else:
            raise ValueError("Invalid email, password, or magic link.")
        return response

    def create_new_draft(self, draft):
        endpoint = f"{self.substack_url}/api/v1/drafts/"
        return self._send_request(endpoint, draft, "POST")

    def edit_draft(self, draft_id, draft):
        endpoint = f"{self.substack_url}/api/v1/drafts/{draft_id}/"
        return self._send_request(endpoint, draft, "PUT")

    def get_draft(self, draft_id):
        endpoint = f"{self.substack_url}/api/v1/drafts/{draft_id}/"
        return self._send_request(endpoint, None, "GET")

    def get_draft_by_title(self, title):
        drafts = self.get_all_drafts()
        filtered_draft = self.filter_drafts_by_title(drafts, title)
        if filtered_draft:
            return filtered_draft
        else:
            return None

    def _send_request(self, endpoint, payload, http_method):
        headers = {
            "Content-Type": "application/json",
            "Cookie": f"substack.sid={self.session_id}",
        }
        #cookies = RequestsCookieJar()
        #cookies.set("substack.sid", self.session_id)

        try:
            if http_method == "POST":
                response = self.client.post(endpoint, headers=headers, json=payload)
            elif http_method == "PUT":
                response = self.client.put(endpoint, headers=headers, json=payload)
            else:
                response = requests.get(endpoint, headers=headers)

            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")


    def get_all_drafts(self):
        endpoint = f"{self.substack_url}/api/v1/post_management/drafts/?offset=0&limit=25&order_by=draft_updated_at&order_direction=desc"
        resp = self._send_request(endpoint, None, "GET")
        return resp.get("posts", [])

    def filter_drafts_by_title(self, drafts, title):
        draft = [draft for draft in drafts if draft.get("draft_title") == title]
        if draft:
            draft = draft[0]
        else:
            return None
        
        draft_obj = self._send_request(f"{self.substack_url}/api/v1/drafts/{draft.get('id')}/", None, "GET")
        return draft_obj

    def update_draft(self, title):
        drafts = self.get_all_drafts()
        filtered_drafts = client.filter_drafts_by_title(drafts, title)
        if filtered_drafts:
            draft_id = filtered_drafts.get("id", -1)
        else:
            exit(1)

        with open("temp.md", "r") as file:
            md_text = file.read()

        doc = convert_to_substack(md_text)

        draft = {
            "draft_title": "test",
            "draft_bylines": [{
                "id": int(self.userId),
                "is_guest": False
            }],
            "draft_body": json.dumps(doc),
            "draft_subtitle": "",
            "draft_podcast_url": "",
            "draft_podcast_duration": None,
            "draft_video_upload_id": None,
            "draft_podcast_upload_id": None,
            "draft_podcast_preview_upload_id": None,
            "draft_voiceover_upload_id": None,
            "section_chosen": False,
            "draft_section_id": None,
            "free_podcast_url": None,
    }
        with open("output1.json", "w") as file:
            json.dump(draft, file, indent=4)
        resp = self.edit_draft(draft_id, draft)
        return resp

    def create_draft(self, title, markdown_text):
        substack_post = convert_to_substack(markdown_text)
        substack_post_json = json.dumps(substack_post)
        # convert to json string
        substack_json = substack_post_json
        draft = {
            "draft_title": title,
            "draft_bylines": [{
                "id": int(self.userId),
                "is_guest": False
            }],
            "draft_body": substack_json,
            "draf_subtitle": "",
            "draft_podcast_url": "",
            "draft_podcast_duration": None,
            "draft_video_upload_id": None,
            "draft_podcast_upload_id": None,
            "draft_podcast_preview_upload_id": None,
            "draft_voiceover_upload_id": None,
            "section_chosen": False,
            "draft_section_id": None,
            "audience": "everyone",
            "type": "newsletter",
        }
        # create a tmp file
        file_name = tempfile.mkstemp()
        tmp_draft = json.dump(draft, open(file_name[1], "w"))
        draft = json.load(open(file_name[1], "r"))
        os.remove(file_name[1])
        new_draft = self.create_new_draft(draft)
        return new_draft

def send_magic_link(email):
    body = {
        "email": email,
        "redirect": "/",
        "for_pub": "",
    }
    endpoint = f"https://substack.com/api/v1/email-login/"
    response = requests.post(endpoint, json=body)
    print("Magic link sent!")


if __name__ == "__main__":

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
    draft_title = "test"

    print(client.get_all_drafts())
    #draft = client.get_draft("144553105")
    #draft = client.create_draft(draft_title, "") or {}
    #client.update_draft(draft.get("draft_title", ""))
    client.update_draft(draft_title)

