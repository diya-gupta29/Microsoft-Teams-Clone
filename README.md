# Microsoft Teams Clone
A one stop web app allowing interactive collaboration through video call and chat feature.


## Technology Stack

 - Django (Python)
 - Django Channels
 - WebRTC
 - WebSockets
 - HTML
 - CSS
 - BootStrap
 - Javascript
 - PostgreSql (Database)

## Features 

 - Login, Sign Up, Reset and Change Password Functionality. 
 - Video Call and Chat Feature.
 - Create Team and Leave team functionality.
 - Special Privileges based on the role (owner or participant) such as delete team, add members and many more.
 - Invite people through mail over a video call.

## Install components
```bash
sudo apt-get update
sudo apt-get install python-pip 
```

### Setting up Virtual Environment 
```bash
sudo pip install virtualenv
python3 -m venv myenv
source myenv/bin/activate
```

### Clone the repo and Install Requirements
```bash
git clone 
cd base_auth_final
pip install -r requirements.txt
```
### Make Changes in the settings.py file
```bash
set up your EMAIL_HOST_USER and EMAIL_HOST_PASSWORD
Install PostgreSQL and provide your own username and password in database.
```

### Running the website locally
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
