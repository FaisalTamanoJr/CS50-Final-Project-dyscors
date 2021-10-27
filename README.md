# dyscors
## Website: https://dyscors.herokuapp.com/
#### Video Demo: https://youtu.be/yv1DG096t0Q
#### Description:
A simple forum made using flask.

The main folder contains four files: config.py, dyscors.py, tests.py, and requirements.txt. The config.py file is used for storing configuration variables that the application will use. Usually, variables such as the secret key, the location of the database, and the option to track changes in the database, can be found here. Dyscors.py will be used to create the app by using the create_app() function in the app folder. Test.py can be used for testing functions that you added. It can help check if the functions in the web application work properly. Lastly, the requirements.txt will help install dependencies for the program.

The app folder contains five different folders and two different files. The five folders are separated based on their uses. The auth folder contains the function for forms and logic for routes. It contains functions used for authentication. For example, functions for signing in and registering. While the errors folder contains functions for handling errors. It includes which template to render and what error code to return when encountering a problem. The main folder contains the main logic for the routes and the main functions that will be used. It contains functions for posting, creating a comment, replying to a comment, viewing the index page, and viewing the different sections or categories. The static folder is used for the style and design of the web application. The templates folder is separated into three parts: main (which is not inside a folder), auth, and errors. The main is the main HTML templates that will be used to render the main web pages. While the auth folder is used for authentication purposes such as logging in and signing up. The error folder contains templates used in error handling. The two files in the app directory are __init__.py and models.py. __init__.py is used for initializing the flask extensions that are used in the flask program. It is also used to create the application by initializing the extensions and registering the different blueprints or the three folders: auth, errors, and main. The models.py will be used for creating and designing the database tables.

The logs folder is where the log files are saved whenever there are errors caught by the program.

Lastly, the migrations folder is used for the flask-migrate extension. It helps manage and update the database. It can be used for upgrading or downgrading the database whenever models.py is altered and flask db migrate command is executed.

The application is separated into multiple folders and blueprints so that when it grows larger, it does not get more difficult to manage. Also, there are three different layouts because they are not very similar and it would be difficult to only use one single layout.

#### Features:
* Users that are signed in can post, comment, and reply to comments
* Profile pages can be viewed even without signing in
* Post and comment history can be viewed in the profile pages
* The most recent posts can be viewed in the index page
* Posts, comments, and replies are sorted based on the time they were posted
* Posts are divided into different sections based on their topics


