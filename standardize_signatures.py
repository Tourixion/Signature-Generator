import json
from jinja2 import Template

def load_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

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
    # Load data
    signatures = load_json('signatures.json')
    example_signature = load_example_signature('example_signature.txt')
    
    # Create template from example signature
    template = Template(example_signature)
    
    # Standardize signatures
    standardized_signatures = standardize_signatures(signatures, template)
    
    # Save standardized signatures
    save_standardized_signatures(standardized_signatures, 'standardized_signatures.txt')

if __name__ == '__main__':
    main()
