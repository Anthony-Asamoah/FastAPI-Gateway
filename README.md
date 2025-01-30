# Brief
A simple FastApi app to serve as an API Gateway.
The aim is to expose as many servers/hosts under a single port.

# Getting Started
- clone the repo
- create a new branch that you can make changes to using the format 'feat/<title>'
- copy '.example.env' file and rename to '.env'
- apply the appropriate values in the new .env file
- navigate to src.config and copy 'expose.example.py' file, then rename it to 'expose.py'
- apply the servers/urls/apis that you want to expose inside the 'available_backends' dictionary
- run pipenv install
- using pipenv shell, run the main script

# Contributing
All contributions to improve, optimize or add new features are gladly welcomed.
Follow these steps to contibute to the project.
- create a feature branch with your changes using this naming convention; 'feat/<title>'
- create a pull request into the dev branch
- patiently wait for a review to be completed
