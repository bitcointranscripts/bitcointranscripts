import os
import re
import yaml
from collections import OrderedDict
import subprocess

class OrderedLoader(yaml.SafeLoader):
    pass

class PreservingOrderedDumper(yaml.SafeDumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(PreservingOrderedDumper, self).increase_indent(flow, False)

    def represent_scalar(self, tag, value, style=None):
        if isinstance(value, str) and '\n' in value:
            return super().represent_scalar(tag, value, style='|')
        return super().represent_scalar(tag, value, style)

def dict_constructor(loader, node):
    return OrderedDict(loader.construct_pairs(node))

OrderedLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    dict_constructor)

def dict_representer(dumper, data):
    return dumper.represent_mapping(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        data.items())

PreservingOrderedDumper.add_representer(OrderedDict, dict_representer)

def process_markdown_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Extract YAML front matter
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if match:
        front_matter_str = match.group(1)
        front_matter = yaml.load(front_matter_str, Loader=OrderedLoader)
        categories = front_matter.pop('categories', None)
        
        if categories:
            # Remove categories from front matter
            new_front_matter = yaml.dump(front_matter, Dumper=PreservingOrderedDumper, allow_unicode=True, default_flow_style=False, indent=2, width=float("inf"))
            new_content = f"---\n{new_front_matter}---\n{content[match.end():]}"
            
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(new_content)
            
            return categories
    
    return None

def update_index_file(index_path, types):
    if os.path.exists(index_path):
        with open(index_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Extract YAML front matter
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if match:
            front_matter = yaml.load(match.group(1), Loader=OrderedLoader)
        else:
            front_matter = OrderedDict()
        
        front_matter['types'] = types
        new_front_matter = yaml.dump(front_matter, Dumper=PreservingOrderedDumper, allow_unicode=True, default_flow_style=False, indent=2, width=float("inf"))
        
        if match:
            new_content = f"---\n{new_front_matter}---\n{content[match.end():]}"
        else:
            new_content = f"---\n{new_front_matter}---\n\n{content}"
        
        with open(index_path, 'w', encoding='utf-8') as file:
            file.write(new_content)
    else:
        with open(index_path, 'w', encoding='utf-8') as file:
            yaml.dump({'types': types}, file, Dumper=PreservingOrderedDumper, allow_unicode=True, default_flow_style=False, indent=2, width=float("inf"))
            file.write('\n')

def process_directory(directory):
    print(f"\nProcessing directory: {directory}")
    all_categories = set()
    files_to_process = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md') and not file.startswith('_index') and not re.match(r'^.*index\.[a-z]{2}\.md$', file):
                file_path = os.path.join(root, file)
                categories = process_markdown_file(file_path)
                if categories:
                    all_categories.update(categories)
        
        # Process only the current directory
        break
    
    if all_categories:
        print("Categories found in this directory:")
        for category in sorted(all_categories):
            print(f"- {category}")
        
        types = input("Enter the types you want to add to the _index.md file (comma-separated): ").split(',')
        types = [t.strip() for t in types]
        
        confirm = input("Do you want to proceed with these changes? (y/n): ").lower()
        if confirm == 'y':
            for file_path in files_to_process:
                process_markdown_file(file_path)
            
            index_path = os.path.join(directory, '_index.md')
            update_index_file(index_path, types)
            
            # Stage changes
            subprocess.run(['git', 'add', directory])
            
            # Commit changes
            # Remove './' from the beginning of the directory path
            clean_directory = directory[2:] if directory.startswith('./') else directory
            commit_message = f"refactor(metadata): convert categories to types in `{clean_directory}`"
            subprocess.run(['git', 'commit', '-m', commit_message])
            
            print(f"Changes in {clean_directory} have been committed.")
        else:
            print("Operation cancelled.")
    
    # Process subdirectories
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            process_directory(item_path)

# Start processing from the current directory
process_directory('.')