import csv
import io
import requests
from jinja2 import Template
import os

def get_gist_content(gist_id, filename):
    gist_token = os.environ['GIST_TOKEN']
    headers = {'Authorization': f'token {gist_token}'}
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
    users_data = []
    for row in csv_reader:
        # Remove any empty keys (which could be caused by trailing commas)
        cleaned_row = {k: v for k, v in row.items() if k}
        users_data.append(cleaned_row)
    return users_data

def generate_signatures(template_str, users_data):
    template = Template(template_str)
    signatures = []
    for user in users_data:
        # Ensure all keys are strings and values are stripped of whitespace
        user = {str(k): v.strip() if isinstance(v, str) else v for k, v in user.items()}
        # Split addresses into a list
        user['addresses'] = [addr.strip() for addr in user.get('Address', '').split('|') if addr.strip()]
        signature = template.render(user)
        signatures.append(signature)
    return signatures

def save_signatures_to_gist(signatures, gist_id, output_filename):
    gist_token = os.environ['GIST_TOKEN']
    headers = {
        'Authorization': f'token {gist_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    separator = "\n\n" + "="*50 + "\n\n"  # Non-code separator
    content = separator.join(signatures)
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
