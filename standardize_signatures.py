import json
import os
import requests
from jinja2 import Template

def load_json_from_gist(gist_id, github_token):
    headers = {'Authorization': f'token {github_token}'}
    response = requests.get(f'https://api.github.com/gists/{gist_id}', headers=headers)
    response.raise_for_status()
    gist = response.json()
    file_content = list(gist['files'].values())[0]['content']
    return json.loads(file_content)

def load_example_signature(filename):
    with open(filename, 'r') as f:
        return f.read()

def standardize_signatures(signatures, template):
    standardized = []
    for sig in signatures:
        standardized.append(template.render(sig))
    return standardized

def save_standardized_signatures(signatures, filename):
    with open(filename, 'w') as f:
        for sig in signatures:
            f.write(sig + '\n\n')

def main():
    # Load data from GitHub Gist
    gist_id = os.environ['GIST_ID']
    github_token = os.environ['GITHUB_TOKEN']
    signatures = load_json_from_gist(gist_id, github_token)
    
    # Load example signature
    example_signature = load_example_signature('example_signature.txt')
    
    # Create template from example signature
    template = Template(example_signature)
    
    # Standardize signatures
    standardized_signatures = standardize_signatures(signatures, template)
    
    # Save standardized signatures
    save_standardized_signatures(standardized_signatures, 'standardized_signatures.txt')

if __name__ == '__main__':
    main()
