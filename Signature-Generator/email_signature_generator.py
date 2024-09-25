import csv
import io
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
    csv_file = io.StringIO(content)
    csv_reader = csv.DictReader(csv_file)
    return list(csv_reader)

def generate_signatures(template_str, users_data):
    template = Template(template_str)
    return [template.render(user) for user in users_data]

def save_signatures_to_gist(signatures, gist_id, output_filename):
    github_token = os.environ['GITHUB_TOKEN']
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    content = "\n\n".join(signatures)
    data = {
        'files': {
            output_filename: {
                'content': content
            }
        }
    }
    response = requests.patch(f'https://api.github.com/gists/{gist_id}', headers=headers, json=data)
    response.raise_for_status()
    print(f"Email signatures saved to Gist: {response.json()['html_url']}")

def main():
    gist_id = os.environ['GIST_ID']
    template = load_template(gist_id, 'email_signature_template.html')
    users_data = load_user_data(gist_id, 'user_data.csv')
    signatures = generate_signatures(template, users_data)
    save_signatures_to_gist(signatures, gist_id, 'generated_signatures.html')
    print("Email signatures generated successfully!")

if __name__ == "__main__":
    main()
