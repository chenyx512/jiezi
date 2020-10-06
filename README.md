# Solved Chinese

*Solve Chinese characters like riddles.*

## File Structure
- `static/` & `templates/` for front end use
-  `learning/` & `accounts/` & `jiezi_admin/` our custom apps for backend use
- `jiezi` django main app

## API generation
We are now using Django REST Framework's self-browsable API served at <https://solvedchinese.org/api_root>. You can also test it locally in your development server.

## Installation
this is supposed to be done on a Ubuntu machine
1. clone this repo
```shell script
git clone git@github.com:solved-chinese/app.git
```
2. Create a conda environment using the `env.yaml` file in project root and activate it:
```shell script
conda env create -f env.yaml
conda activate jiezi
```
3. Setup PostgresSQL:
install PostgresSQL <https://www.postgresql.org/download/linux/ubuntu/>
setup the database to match `jiezi.settings.DATABASES`:
``` shell script
sudo -u postgres psql
postgre# \password postgres (use this to change the password of postgres to 'jiezi')
```

4. Create your own secret files:
    1. Generate your own django secret_key, in python:  
    
   ``` python
   from django.core.management.utils import get_random_secret_key  
   get_random_secret_key() # the returned value is your secret key
   ```  
   
    2. Create `jiezi_secret/secret.py` using your secret key:  
    
    ```python
   """This file is suppose to keep secret variables """
    
    SECRET_KEY = 'YOUR_SECRET_KEY'
    
    # This should store jiezi_secret or local database, and it will update setting
    # DATABASES (you may override default database if necessary)
    DATABASES = {
    }
   ```
   
   3. get `jiezi_secret/datafile_service_account.json` from us, this is used to access our google drive data 

5. Make the required migrations
```shell script
python manage.py migrate
```

6. For the setup of Celery and Redis, reference [wiki page](https://github.com/solved-chinese/app/wiki/Celery-and-Redis-Installation-for-progress-bar) Note that Celery doesn't work with Windows! 
  


7. Locally run the development server
```shell script
python manage.py runserver
```
