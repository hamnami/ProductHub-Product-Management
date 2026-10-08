# ProductHub — Mini Product Management Website

A clean Django + SQLite inventory management website built for the mini product-management task.

## Features
- Add, edit and delete products
- Product name, SKU, description, price and stock management
- Upload product images
- Manage categories (add/edit/delete)
- Search products by name, SKU or description
- Filter by category and stock status
- Product details page with sales history
- Record sales and automatically reduce stock
- Dashboard with inventory value, stock counts and recent sales
- Django admin panel

## Tech Stack
- Python
- Django
- SQLite
- HTML/CSS
- Pillow for image uploads

## Run locally
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
Open http://127.0.0.1:8000/

## Optional admin
```bash
python manage.py createsuperuser
```
Then visit http://127.0.0.1:8000/admin/

## Submission note
The project is intentionally self-contained and uses SQLite, so no separate database server is required.
