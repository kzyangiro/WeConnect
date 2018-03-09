[![Build Status](https://travis-ci.org/kzyGit/WeConnect.svg?branch=api)](https://travis-ci.org/kzyGit/WeConnect)

[![Coverage Status](https://coveralls.io/repos/github/kzyGit/WeConnect/badge.svg?branch=master)](https://coveralls.io/github/kzyGit/WeConnect?branch=master)
<h3>WeConnect Api</h3>

This is an api that is to manage data access between various endpoints of the WeConnect application. WeConnect Application is an application that links users to businesses. A viewer is able to view avaiable businesses, view their profiles and post reviews about a business. A user is also able to create a business and manage the businesses by either updating or deleting.<br>
WeConnect Api contains the endpoints that are used in acessing and managing information about the user, businesses and their reviews

<h4>Technology used</h4>
<ul>
  <li>Flask Microframework</li>
  <li>Restful Api</li>
  <li>Python 3.6.0</li>
 </ul>

<h4>Installation</h4>
Install python, create and activate a virtual environmet.<br>
Ensure you have postman installed.<br>
Run requirements.txt to install the necessary packages. To do this run > pip install -r requirements.txt 

<h4>Running the api</h4>

  - Navigate to the projects directory: WeConnect, then run command > python run.py<br>
  - Open postman, add the first default url > http://127.0.0.1:5000 <br>
  - Add the route of your endpoint to the default url<br>
      Example: http://127.0.0.1:5000/api/v1/businesses <br>

Select body section on the postman navigation tabs, select raw, then Json, add parameters then
Send request


<h4>Unit Testing</h4>
  - Use pytest for running the tests<br>
  - To run tests use: pytest

<h4>UI Templates</h4>
The UI is hosted on github pages.
Link: https://kzygit.github.io/designs/UI/index.html

<h4>Features</h4>
  - A user can create an account<br>
  - User can login<br>
  - User can add businesses, update, delete and also view all businesses and business by ID.<br>





