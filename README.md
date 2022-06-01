# aci_backend

# Installation of requirements

python -m pip install -r requirements.txt

python manage.py makemigrations

python manage.py makemigrations api

python manage.py migrate

## Scripts (Bash shell only)

you can bash script on windows to easily

```bash
scripts/format.sh # to easily format all python code
scripts/pyenv.sh # to easily setup all environment
scripts/migrator.sh # to easily migrate database structure & create new user
```
# Run server
 * Don't forgot to run your python environnement
 * Don't forgot to launch mysql server

python manage.py runserver
