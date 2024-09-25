import json
import requests
from jinja2 import Template
import os

def get_gist_content(gist_id, filename):
    github_token = os.environ['GITHUB_TOKEN']
    headers = {'Authorization': f'token {github_token}'}
    response = requests.get(f'https://api.github.com/gists/{gist_id}', headers=headers)
    response.raise_for_status()
    gist = response.json()
    return gist['files'][filename]['content']

def load_template(gist_id, template_filename):
    return get_gist_content(gist_id, template_filename)

def load_user_data(gist_id, user_data_filename):
    content = get_gist_content(gist_id, user_data_filename)
    return json.loads(content)

def generate_signature(template_str, user_data):
    template = Template(template_str)
    return template.render(user_data)

def save_signature_to_gist(signature, gist_id, output_filename):
    github_token = os.environ['GITHUB_TOKEN']
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    data = {
        'files': {
            output_filename: {
                'content': signature
            }
        }
    }
    response = requests.patch(f'https://api.github.com/gists/{gist_id}', headers=headers, json=data)
    response.raise_for_status()
    print(f"Email signature saved to Gist: {response.json()['html_url']}")

def main():
    gist_id = os.environ['GIST_ID']
    template = load_template(gist_id, 'email_signature_template.html')
    user_data = load_user_data(gist_id, 'user_data.json')
    signature = generate_signature(template, user_data)
    save_signature_to_gist(signature, gist_id, 'generated_signature.html')
    print("Email signature generated successfully!")

if __name__ == "__main__":
    main()
