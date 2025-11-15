# MPress Deployment Guide for PythonAnywhere

## Step-by-Step Deployment Instructions

### **STEP 1: Prepare Your Project Locally**

1. **Update `.gitignore`** (if using Git):
   ```
   *.pyc
   __pycache__/
   db.sqlite3
   .DS_Store
   venv/
   .env
   *.egg-info/
   dist/
   build/
   .venv
   node_modules/
   *.log
   ```

2. **Create a `.env` file for PythonAnywhere** (don't commit this):
   ```
   SECRET_KEY=your-super-secret-key-here-generate-a-new-one
   DEBUG=False
   ALLOWED_HOSTS=yourusername.pythonanywhere.com
   ```

3. **Generate a new SECRET_KEY** (run in Python):
   ```python
   from django.core.management.utils import get_random_secret_key
   print(get_random_secret_key())
   ```

4. **Test locally**:
   ```powershell
   python manage.py check
   python manage.py collectstatic --noinput
   ```

---

### **STEP 2: Prepare for Deployment**

1. **Update your requirements.txt** to include all dependencies:
   ```bash
   pip freeze > requirements.txt
   ```

2. **Verify `requirements.txt` contains**:
   - Django==5.2.8
   - gunicorn==21.2.0
   - whitenoise
   - Pillow>=10.0
   - Any other packages your project uses

3. **Create `pythonanywhere_settings.py`** (optional, for per-environment settings):
   - This file will be used on PythonAnywhere only
   - Create at: `MPress/pythonanywhere_settings.py`

---

### **STEP 3: Push to GitHub**

1. **Initialize Git** (if not already done):
   ```powershell
   git init
   git add .
   git commit -m "Initial commit - ready for PythonAnywhere deployment"
   ```

2. **Push to GitHub**:
   ```powershell
   git remote add origin https://github.com/yourusername/mpress.git
   git push -u origin main
   ```

---

### **STEP 4: Create PythonAnywhere Account & Setup**

1. **Sign up at https://www.pythonanywhere.com**

2. **Go to "Web" tab** → Click "Add a new web app"
   - Choose "Manual configuration"
   - Select **Python 3.10** (or your preferred version)
   - Complete the setup

3. **Note your directory**:
   - It will be something like: `/home/yourusername/mpress`

---

### **STEP 5: Clone Your Project on PythonAnywhere**

1. **Open a Bash Console** on PythonAnywhere

2. **Clone your repository**:
   ```bash
   cd /home/yourusername
   git clone https://github.com/yourusername/mpress.git
   cd mpress
   ```

3. **Create a virtual environment**:
   ```bash
   python3.10 -m venv venv
   source venv/bin/activate
   ```

4. **Install dependencies**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

---

### **STEP 6: Configure PythonAnywhere Web App**

1. **Go to Web tab** on PythonAnywhere

2. **Edit the WSGI file**:
   - Click on your web app
   - Edit WSGI configuration file (usually `/home/yourusername/mpress/mpress_wsgi.py`)
   - Replace content with:

   ```python
   import os
   import sys
   
   # Add your project directory to the Python path
   path = '/home/yourusername/mpress'
   if path not in sys.path:
       sys.path.append(path)
   
   # Set Django settings module
   os.environ['DJANGO_SETTINGS_MODULE'] = 'MPress.settings'
   
   # Load environment variables (if using .env file)
   from pathlib import Path
   env_file = Path('/home/yourusername/mpress/.env')
   if env_file.exists():
       from dotenv import load_dotenv
       load_dotenv(env_file)
   
   # Import Django WSGI application
   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```

3. **Set up Static Files**:
   - In PythonAnywhere Web tab, under "Static files":
     - URL: `/static/`
     - Directory: `/home/yourusername/mpress/staticfiles`
   - Click "Add another"
     - URL: `/media/`
     - Directory: `/home/yourusername/mpress/media`

---

### **STEP 7: Configure Database**

1. **Run migrations** in PythonAnywhere Bash Console:
   ```bash
   cd /home/yourusername/mpress
   source venv/bin/activate
   python manage.py migrate
   ```

2. **Create superuser**:
   ```bash
   python manage.py createsuperuser
   ```

3. **Collect static files**:
   ```bash
   python manage.py collectstatic --noinput
   ```

---

### **STEP 8: Configure Environment Variables**

1. **On PythonAnywhere Web tab**, scroll down to "Web app security"

2. **Add environment variables**:
   - `SECRET_KEY`: Your generated secret key
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: `yourusername.pythonanywhere.com`

   Alternatively, use a `.env` file in `/home/yourusername/mpress/`

---

### **STEP 9: Update ALLOWED_HOSTS**

1. **In `MPress/settings.py`**, add your PythonAnywhere domain:
   ```python
   ALLOWED_HOSTS += ['yourusername.pythonanywhere.com']
   ```

2. **Push changes to GitHub**:
   ```powershell
   git add .
   git commit -m "Configure for PythonAnywhere deployment"
   git push
   ```

3. **Pull changes on PythonAnywhere** (in Bash Console):
   ```bash
   cd /home/yourusername/mpress
   git pull origin main
   ```

---

### **STEP 10: Reload Web App**

1. **Go to Web tab** on PythonAnywhere

2. **Click the Green "Reload" button** at the top right

3. **Visit your site**: `https://yourusername.pythonanywhere.com`

---

## Troubleshooting

### **500 Error or Blank Page**

1. **Check error logs** in PythonAnywhere Web tab (scroll down to "Log Files")
2. **Check Django logs**:
   ```bash
   cd /home/yourusername/mpress
   tail -f /var/log/yourusername.pythonanywhere.com.error.log
   ```

3. **Test locally**:
   ```bash
   python manage.py runserver
   ```

### **Static Files Not Loading**

1. **Run collectstatic again**:
   ```bash
   python manage.py collectstatic --noinput
   ```

2. **Verify static file paths** in Web tab match your `STATIC_ROOT`

3. **Clear browser cache** (Ctrl+Shift+Delete)

### **Database Lock Error**

1. **SQLite has limitations** on PythonAnywhere
2. **Consider switching to PostgreSQL**:
   ```bash
   pip install psycopg2-binary
   ```
   Update `DATABASES` in settings.py with PostgreSQL credentials

### **Module Import Errors**

1. **Verify all dependencies** are in `requirements.txt`:
   ```bash
   pip freeze
   ```

2. **Reinstall packages**:
   ```bash
   pip install -r requirements.txt --force-reinstall
   ```

---

## Production Checklist

- [ ] `DEBUG = False` in production
- [ ] New `SECRET_KEY` generated and set
- [ ] `ALLOWED_HOSTS` updated with your domain
- [ ] Database migrations run
- [ ] Static files collected
- [ ] Superuser created
- [ ] Security settings enabled in `settings.py`
- [ ] Environment variables configured
- [ ] `.env` file added to `.gitignore`
- [ ] WSGI file correctly configured
- [ ] Web app reloaded

---

## Useful PythonAnywhere Commands

```bash
# Activate virtual environment
source /home/yourusername/mpress/venv/bin/activate

# Check Python version
python --version

# Check Django version
python -c "import django; print(django.get_version())"

# Test Django setup
python manage.py check

# Run shell
python manage.py shell

# View logs
tail -f /var/log/yourusername.pythonanywhere.com.error.log
```

---

## Next Steps

1. **Set up HTTPS** (PythonAnywhere provides free SSL)
2. **Configure email** for password reset and notifications
3. **Set up backups** for your database
4. **Monitor performance** using PythonAnywhere's dashboard

Good luck with your deployment! 🚀
