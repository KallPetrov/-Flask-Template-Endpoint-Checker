import os
import re
import sys

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'templates')
VIEWS_FILE = os.path.join(os.path.dirname(__file__), 'views.py')

# Ensure UTF-8 output encoding for terminals that default to something else
if sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

# 1. Extract all endpoints from views.py
route_pattern = re.compile(r"@views_bp\.route\(['\"](.*?)['\"]")

def get_defined_view_endpoints():
    endpoints = set()
    with open(VIEWS_FILE, encoding='utf-8') as f:
        for line in f:
            match = route_pattern.search(line)
            if match:
                route = match.group(1)
                parts = route.strip('/').split('/')
                if not parts or parts[-1] == '':
                    continue
                if '<' in parts[-1]:
                    # Example: /something/<int:id>/edit
                    if len(parts) > 1:
                        endpoint = f"views.{parts[0]}_{parts[-1]}"
                    else:
                        endpoint = f"views.{parts[-2]}_{parts[-1]}"
                else:
                    endpoint = f"views.{parts[-1]}"
                endpoints.add(endpoint)
    return endpoints

# 2. Extract all used endpoints from Jinja templates
url_for_pattern = re.compile(r"url_for\(['\"]([a-zA-Z0-9_\.]+)['\"]")

def get_used_template_endpoints():
    used_endpoints = set()
    for root, _, files in os.walk(TEMPLATES_DIR):
        for file in files:
            if file.endswith('.html'):
                with open(os.path.join(root, file), encoding='utf-8') as f:
                    for line in f:
                        for match in url_for_pattern.finditer(line):
                            used_endpoints.add(match.group(1))
    return used_endpoints

if __name__ == "__main__":
    defined_endpoints = get_defined_view_endpoints()
    used_endpoints = get_used_template_endpoints()

    print("\nEndpoints used in templates but NOT found in views.py:")
    for endpoint in sorted(used_endpoints):
        if endpoint not in defined_endpoints:
            print(f"  - {endpoint}")

    print("\nAll defined endpoints in views.py:")
    for endpoint in sorted(defined_endpoints):
        print(f"  - {endpoint}")
