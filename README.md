# Movies Bookmark Web Application

## Description
The web app is built with Python Flask framework, which allows users to store, manage and share their movie watching history. The web app persists user data in Postgres database and implements a full CRUD (create, read, update and delete) RESTful APIs and UI to movies users watched. The app also offers a third-party authentication & authorization service such that users can login/register via their Google or Facebook Account. I also configured and published the application on an Ubuntu server offered by AWS Lightsail. (https://github.com/junyan59/Linux-server-configuration)

## Skills used for this project
- Python
- Flask
- HTML
- CSS
- SQLAchemy
- OAuth2.0
- Facebook / Google Login

## Some things you might need
- [Vagrant](https://www.vagrantup.com/)
- [Udacity Vagrantfile](https://github.com/udacity/fullstack-nanodegree-vm)
- [VirtualBox](https://www.virtualbox.org/wiki/Downloads)

## Getting Started
1. Install Vagrant & VirtualBox
2. Clone the Udacity Vagrantfile
3. Go to Vagrant directory and either clone this repo or download and place zip here
3. Launch the Vagrant VM (`vagrant up`)
4. Log into Vagrant VM (`vagrant ssh`)
5. Navigate to `cd/vagrant` as instructed in terminal
6. Setup application database `python database_setup.py`
7. *Insert example items data `python example_items.py`
8. Run application using `python __init__.py`
9. Access the application locally using http://localhost:8000

*Optional step(s)

## Using Google Login
To get the Google login working there are a few additional steps:

1. Go to [Google Dev Console](https://console.developers.google.com)
2. Sign up or Login if prompted
3. Go to Credentials
4. Select Create Crendentials > OAuth Client ID
5. Select Web application
6. Enter name 'Movies Bookmark'
7. Authorized JavaScript origins = 'http://localhost:8000'
8. Authorized redirect URIs = 'http://localhost:8000/login' && 'http://localhost:8000/gconnect'
9. Select Create
10. Copy the Client ID and paste it into the `data-clientid` in login.html
11. On the Dev Console Select Download JSON
12. Rename JSON file to client_secrets.json
13. Place JSON file in movies-bookmark directory that you cloned from here
14. Run application using `python __init__.py`

## JSON Endpoints
The following are open to the public:

Catalog JSON: `/catalog/JSON`
    - Displays the whole movies catalog, categories and all items

Category Items JSON: `/catalog/<int:category_id>/items/JSON`
    - Displays movie items for a specific movie category

Category Item JSON: `/catalog/<int:category_id>/items/<int:item_id>/JSON`
    - Displays a specific movie category item
