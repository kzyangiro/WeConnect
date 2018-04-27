[![Build Status](https://travis-ci.org/kzyGit/WeConnect.svg?branch=api)](https://travis-ci.org/kzyGit/WeConnect)
[![Coverage Status](https://coveralls.io/repos/github/kzyGit/WeConnect/badge.svg?branch=master)](https://coveralls.io/github/kzyGit/WeConnect?branch=master)
<a href="https://codeclimate.com/github/codeclimate/codeclimate/maintainability"><img src="https://api.codeclimate.com/v1/badges/a99a88d28ad37a79dbf6/maintainability" /></a>
<a href="https://codeclimate.com/github/codeclimate/codeclimate/test_coverage"><img src="https://api.codeclimate.com/v1/badges/a99a88d28ad37a79dbf6/test_coverage" /></a>

<h3>WeConnect Api</h3>

This is an api that is to manage data access between various endpoints of the WeConnect application. WeConnect Application is an application that links users to businesses. A viewer is able to view avaiable businesses, view their profiles and post reviews about a business. A user is also able to create a business and manage the businesses by either updating or deleting.<br>
WeConnect Api contains the endpoints that are used in acessing and managing information about the user, businesses and their reviews<br>

<h4>UI Templates</h4>
The UI is hosted on github pages.<br>
Link: https://kzygit.github.io/designs/UI/index.html

<h4>Technology used</h4>
<ul>
  <li>Flask Microframework</li>
  <li>Restful Api</li>
  <li>Python 3.6.0</li>
 </ul>

<h4>Application Setup</h4>

First, clone or download the project from github. <br>

```sh
https://github.com/kzyGit/WeConnect.git
```
Setup a virtual Environment<br>
```sh
$ export FLASK_APP="run.py"
$ export APP_SETTINGS="development"
$ export SECRET="your-secret"
$ export DATABASE_URL="postgresql://localhost/flask_api" 

```
Install dependencies<br>
```sh
pip install -r requirements.txt
```

<h4>Running the api</h4>

  - Navigate to the projects directory: WeConnect, then run command
  ```sh
  python run.py
  ```
  - Open postman, add the first default url > http://127.0.0.1:5000 <br>
  - Add the route of your endpoint to the default url<br>
      Example: http://127.0.0.1:5000/api/v1/businesses <br>

Select body section on the postman navigation tabs, select raw, then Json, add parameters then
Send request <br><br>
For the endpoints that require authorization,you need to first register as a user: http://127.0.0.1:5000/api/v1/auth/register <br>login using the login endpoint > http://127.0.0.1:5000/api/v1/auth/login <br>

Copy the access token generated, fill in as authorisation "Bearer Token" then you can proceed to access the endpoints


<h4>Unit Testing</h4>
  - Use pytest or nosetests for running the tests<br>
  - To run tests using pytest, use the command: $ pytest



<h4>Features</h4>
  - A user can create an account<br>
  - Registered User can login and logout<br>
  - Logged in User can add businesses, update, delete and also view all his registered businesses<br>
  - User can view all businesses, filter businesses by id, name, location, category and can also indicate the limit of businesses to display<br>
  - Authenticated user can reset password.<br>
  - User can add reviews for a business and also view reviews for businesses by business ID.
  
<h4>Author</h4>
  - Kezzy Ang'iro<br>




