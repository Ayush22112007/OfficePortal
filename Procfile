web: python manage.py migrate && gunicorn Myproject.wsgi:application --bind 0.0.0.0:$PORT

git add Procfile  # or just Procfile if not using runserver.py
git commit -m "Add Procfile and runserver script for Railway deployment"
git push origin main

