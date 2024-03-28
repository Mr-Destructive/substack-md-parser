from os import environ
import markdown
import requests
import json

from parser import parse_markdown


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
    return {
        "type": NodeType.Doc,
        "content": [{
            "type": NodeType.Paragraph,
            "content": [
                {
                    "type": NodeType.Text,
                    "text": html_content
                }
            ]
        }]
    }
def convert_to_substack(md_text):
    #html_content = parse(md_text)
    #substack_post = parse_html_to_substack(html_content)
    contents = parse_markdown(md_text)
    substack_post = {
        "type": NodeType.Doc,
        "content": contents
    }
    print(substack_post)
    return substack_post

class SubstackClient:
    def __init__(self, session_id, substack_name):
        self.session_id = session_id
        self.substack_name = substack_name
        self.substack_url = f"https://{self.substack_name}.substack.com"

    def create_new_draft(self, draft):
        endpoint = f"{self.substack_url}/api/v1/drafts/"
        return self._send_request(endpoint, draft, "POST")

    def edit_draft(self, draft_id, draft):
        endpoint = f"{self.substack_url}/api/v1/drafts/{draft_id}/"
        return self._send_request(endpoint, draft, "PUT")

    def get_draft(self, draft_id):
        endpoint = f"{self.substack_url}/api/v1/drafts/{draft_id}/"
        return self._send_request(endpoint, None, "GET")

    def _send_request(self, endpoint, payload, http_method):
        headers = {
            "Content-Type": "application/json",
            "Cookie": f"substack.sid={self.session_id};"
        }
        #cookies = RequestsCookieJar()
        #cookies.set("substack.sid", self.session_id)

        try:
            if http_method == "POST":
                response = requests.post(endpoint, headers=headers, json=payload)
            elif http_method == "PUT":
                response = requests.put(endpoint, headers=headers, json=payload)
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
        return [draft for draft in drafts if draft.get("draft_title") == title]

    def update_draft(self, title):
        drafts = self.get_all_drafts()
        filtered_drafts = client.filter_drafts_by_title(drafts, title)
        if filtered_drafts:
            draft_id = filtered_drafts[0].get("id", -1)
        else:
            exit(1)

        with open("temp.md", "r") as file:
            md_text = file.read()

        doc = convert_to_substack(md_text)

        draft = {
            "draft_title": "test",
            "draft_bylines": [{
                "id": userId
            }],
            "draft_body": json.dumps(doc)
        }
        with open("output.json", "w") as file:
            json.dump(draft, file, indent=4)
        resp = self.edit_draft(draft_id, draft)
        return resp

    def create_draft(self, markdown_text):
        substack_post = convert_to_substack(markdown_text)
        substack_post_json = json.dumps(substack_post)
        new_draft = self.create_new_draft(substack_post_json)
        return new_draft


if __name__ == "__main__":

    from dotenv import load_dotenv
    load_dotenv()
    sessionID = environ.get("SUBSTACK_SESSION_ID")
    userId = environ.get("SUBSTACK_USER_ID")
    substackName = environ.get("SUBSTACK_NAME")
    client = SubstackClient(sessionID, substackName)
    draft_title = "test"

    #draft = client.create_draft("test") or {}
    #client.update_draft(draft.get("draft_title", ""))
    client.update_draft(draft_title)

