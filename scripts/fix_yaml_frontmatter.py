import os
import re
import yaml
import traceback

def extract_yaml_front_matter(content):
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if match:
        return match.group(1)
    return None

def fix_yaml_issues(yaml_content):
    # Fix too few spaces after comma
    yaml_content = re.sub(r',(\S)', r', \1', yaml_content)
    
    # Fix too many spaces after colon
    yaml_content = re.sub(r':\s{2,}', r': ', yaml_content)
    
    # Fix too many spaces inside brackets
    yaml_content = re.sub(r'\[\s+', r'[', yaml_content)
    yaml_content = re.sub(r'\s+\]', r']', yaml_content)
    
    # Fix too many spaces after hyphen
    yaml_content = re.sub(r'^\s*-\s{2,}', r'- ', yaml_content, flags=re.MULTILINE)
    
    # Fix indentation (assuming 2 spaces per level)
    lines = yaml_content.split('\n')
    fixed_lines = []
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith('-'):
            indent = len(line) - len(stripped)
            fixed_lines.append(' ' * indent + '- ' + stripped[2:].lstrip())
        else:
            fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)

def process_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        yaml_match = re.match(r'^(---\s*\n)(.*?)(\n---\s*\n)', content, re.DOTALL)
        if yaml_match:
            start, yaml_content, end = yaml_match.groups()
            fixed_yaml = fix_yaml_issues(yaml_content)
            
            new_content = f"{start}{fixed_yaml}{end}{content[yaml_match.end():]}"
            
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(new_content)
            print(f"Fixed YAML front matter in {file_path}")
        else:
            print(f"No YAML front matter found in {file_path}")
    except Exception as e:
        print(f"Error processing file: {file_path}")
        print(f"Error message: {str(e)}")
        print("Traceback:")
        traceback.print_exc()

def main():
    for root, _, files in os.walk('.'):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                process_file(file_path)

if __name__ == "__main__":
    main()