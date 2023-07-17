# Blogging-Portal
A blogging website where user can create blog, like blog and comment on it 

## Getting Started: 🚀

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites 📋
1. first of all, You need to install python for running pip command
2. create a project folder  

### Local Development
1. Clone the repository inside this folder
```bash
https://github.com/divyanshkumarworks/Blogging-Portal.git
```
2. Create Virtual Environment
```bash
python -m venv venv
```
3. Activate the environment
```bash
source /venv/bin/activate
```

4. Install Dependencies
```bash
pip3 install -r requirements.txt
```
5. Make migrations using
```bash
python manage.py makemigrations
```

5. Migrate Database
```bash
python manage.py migrate
```
6. Create a superuser
```bash
python manage.py createsuperuser
```
7. Run server using
```bash
python manage.py runserver
```

### Credits

- I built this to start learning Django
- This project is an extension of the project built by [Corey Schafer](https://www.coreyms.com)
- link for the full django blog-app tutorial [Django Tutorial: Corey Schafer on YouTube](https://youtube.com/playlist?list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH)
- explained very well hope you're going to enjoy it.
