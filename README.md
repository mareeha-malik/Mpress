MPress - Minimal pastel Django blog

Quick-start:

1. Create a virtualenv and install requirements:

   python -m venv venv; .\venv\Scripts\activate; pip install django

2. Run migrations and create superuser:

   python manage.py migrate
   python manage.py createsuperuser

3. (Optional) Create sample data:

   python manage.py shell < manage_sample_data.py

4. Run the server:

   python manage.py runserver

Optional Tailwind build:
 - This project uses the Tailwind CDN for the quick demo UI. For a production build or to use Tailwind utilities in generated CSS, install Node and run:
   - `npm install`
   - `npm run build:css`
 - That will write `static/css/tailwind.css` which you can include in `base.html` instead of the CDN script.

Pillow and images (Windows):
 - If you plan to upload/process images with ImageField, install Pillow. On Windows it's easiest to install a prebuilt wheel or run:
   - `pip install --upgrade pip setuptools wheel`
   - `pip install Pillow`
 - If you run into build issues, consider installing the official binary or using a Windows wheel from the Python Packaging Index.

Admin account:
 - The sample data script creates a user `admin` with password `password` (only if the user didn't already exist). Use `python manage.py changepassword admin` to reset.
 - If you need to promote an existing user to admin, run:
   - `python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='youruser').update(is_staff=True,is_superuser=True)"`

Design:
Uses Tailwind via CDN for quick demo and soft pastel color variables in `templates/base.html`.

Notes:
- This is a demo scaffold. For production, install and configure Tailwind properly, secure SECRET_KEY, and adjust DEBUG/ALLOWED_HOSTS.
- Pillow (Python Imaging Library) is optional and only required if you plan to upload image files via the admin or forms. To install Pillow locally in your virtualenv, run:

   ```powershell
   .\venv\Scripts\python.exe -m pip install Pillow
   ```

   If you encounter build issues when installing Pillow on Windows, try upgrading pip/setuptools/wheel first:

   ```powershell
   .\venv\Scripts\python.exe -m pip install --upgrade pip setuptools wheel
   .\venv\Scripts\python.exe -m pip install Pillow
   ```
