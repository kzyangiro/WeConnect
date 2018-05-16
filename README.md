[![Build Status](https://travis-ci.org/kzyGit/WeConnect.svg?branch=ft-pagination)](https://travis-ci.org/kzyGit/WeConnect)
[![Coverage Status](https://coveralls.io/repos/github/kzyGit/WeConnect/badge.svg?branch=challenge-3)](https://coveralls.io/github/kzyGit/WeConnect?branch=ft-challenge-3)
<a href="https://codeclimate.com/github/codeclimate/codeclimate/maintainability"><img src="https://api.codeclimate.com/v1/badges/a99a88d28ad37a79dbf6/maintainability" /></a>
<!-- <a href="https://codeclimate.com/github/codeclimate/codeclimate/test_coverage"><img src="https://api.codeclimate.com/v1/badges/a99a88d28ad37a79dbf6/test_coverage" /></a> -->

<h3>WeConnect</h3>

WeConnect is an application that links individuals to businesses. A user is able to view avaiable businesses, view their profiles and reviews and also create an account. An authorised user is able to create a business and manage the businesses by either updating or deleting as well as adding reviews to businesses.<br><br>
Link to WeConnect design template: https://kzygit.github.io/designs/UI/index.html<br><br>
Link to WeConnect API documentation: https://app.swaggerhub.com/apis/Andela19/WeConnect/1.0.0<br> 

<h4>Technology used</h4>
<ul>
  <li>Flask Microframework</li>
  <li>Restful Api</li>
  <li>Python 3.6.0</li>
 </ul>

<h4>Installation and Setup</h4>

Create and activate virtual environment:<br>

 ```sh
python3 -m venv env
source ./env/bin/activate 
 ```
Clone or download the api from github. To clone:<br>

```sh
git clone https://github.com/kzyGit/WeConnect.git
```
Move into our WeConnect directory <br>
 
 ```sh
 cd WeConnect
 ```
Install Dependencies: run requirements file<br>
 
 ```sh
 pip install -r requirements.txt
 ```
<h4>Running the api</h4>

- To run the application use the comand:<br>
```sh
python run.py
```
<br>

- Once running, open postman and add the first url: http://127.0.0.1:5000 <br>
- Add the route of your endpoint to the default url: Example: http://127.0.0.1:5000/api/v1/businesses <br>


- Select body section on the postman navigation tabs, select raw, then Json, add parameters as indicated in the route methods then Send request


<h4>Unit Testing</h4>
  - Use pytest or nosetests for running the tests<br>
  - Using pytest to run tests:<br>

  ```sh
  pytest
  ```

<h4>UI Templates</h4>
The UI is hosted on github pages. Link: https://kzygit.github.io/designs/UI/index.html

<h4>Features</h4>

  <ul>
  <li>A user can create an account</li>
  <li>Registered user can login, reset password,logout, add a business, manage the businesses and add business reviews</li>
  <li>All sers can view businesses and their reviews</li>
  </ul>

<h4> Api Endpoints </h4>
<br>
<table>
  <tr><td><b>Functionality</b></td><td><b>Endpoint</b></td></tr>

<tr><td>Create a new user</td><td>POST /api/v1/auth/register</td></tr>
<tr><td>Log in a registered User</td><td>POST /api/v1/auth/login</td></tr>
<tr><td>Logout a User</td><td>POST /api/v1/auth/logout</td></tr>
<tr><td>Password Reset</td><td>POST /api/v1/auth/reset-password</td></tr>
<tr><td>Register a business</td><td>POST /api/v1/businesses</td></tr>
<tr><td>Update a business</td><td>PUT /api/v1/businesses/<businessId></td></tr>
<tr><td>Delete a Business</td><td>DELETE /api/v1/businesses/<businessId></td></tr>
<tr><td>Search a business by name</td><td>GET /api/v1/businesses/<q></td></tr>
<tr><td>Add a business review</td><td>POST /api/v1/businesses/<businessId>/review</td></tr>
<tr><td>Get reviews of a business</td><td>GET /api/v1/businesses/<businessId>/review</td></tr>

</table>

<b> Author </b>: Kezzy Ang'iro




