# 🔍 Flask Template Endpoint Checker

This script scans your Flask project to detect any `url_for(...)` endpoint references in HTML templates that **do not have a corresponding route in `views.py`**.

It helps you identify missing views that are still referenced by the frontend — ideal for keeping templates and backend views in sync.

---

## 📁 Project Structure Assumptions

- `views.py` – contains Flask routes with `@views_bp.route(...)`.
- `templates/` – a folder containing your Jinja2 `.html` templates.

These are assumed to be in the same directory as the script.

---

## 🧠 What the Script Does

### 1. Parses Flask Routes from `views.py`

It uses regex to find routes like:

```python
@views_bp.route('/orders/<int:id>/edit')
````

Then converts them into endpoint-style strings such as:

```
views.orders_edit
```

---

### 2. Parses `url_for(...)` Calls from Templates

Searches all `.html` files under the `templates/` directory for lines like:

```html
<a href="{{ url_for('views.orders_edit', id=5) }}">
```

It collects all such endpoint references.

---

### 3. Compares Both Lists

* Lists all endpoints **used in templates but missing in `views.py`**.
* Lists all endpoints that **exist** in `views.py`.

---

## 📋 Example Output

```
Used endpoints in templates that DO NOT exist in views.py:
  - views.invoice_edit
  - views.asset_delete

All defined endpoints in views.py:
  - views.asset_edit
  - views.asset_list
  - views.invoice_list
```

---

## ▶️ How to Run

```bash
python check_template_endpoints.py
```

---

## 🛠️ Requirements

* Python 3.6+
* Flask project using `views_bp` as the blueprint
* UTF-8 terminal output (auto-configured)

---

## ⚠️ Notes

* Only works with routes declared using `@views_bp.route(...)`.
* Doesn't parse more complex Flask routing logic or dynamic blueprint names.
* It assumes a consistent naming pattern to map URLs to endpoint names (e.g. `/users/list` → `views.users_list`).

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📬 Contact

For issues or suggestions:
**Author:** \[Your Name]
**Email:** \[[lab@hexagon-lab.com](mailto:lab@hexagon-lab.com)]

