# Code Structure Architecture

Last Update `19 feb 2025`

Most of the code is located at www this is because we mainly have a web application, theres db/ where you can see the database migrations, at the root there is docker-compose, this is the best start for local development and Makefile where that is for shotcuts.

## www

This is divided into two parts api and webapp they share the same flask app.

### api

the underlaying architecture is vertical slicing where we have onion base structure but divided by domain driven modules and The main folders are.

* application: integration layer here we will consice usecases import everything required for the usecas, example get_user_list will import user_repository,db_connection.
* domain: here is everything related to the objects that the domain requires example the user domain requires this entities user,credentials,sso_provider this dto's UserCredential this convines user and credentials, finaly we have services where our business logic will live.
* infraestructure: think of this layer as everything that needs to request something from the outside, query db, integrate with other webAPIs, integrate with system APIs etc.

### webapp

This structure is trickier as it isn't a defined architecture as the API, but its following the same domain driven design principle.

* modules: All the python code needed for template, sometimes we access API applications directly, other times we access using the web endpoint.
* static: all the files required by templates, pictures, js, css.
* templates: our html files that will be render, this trys to use component base structure to avoid making gigantic files

## db

The migration system is flyway and we have a shortcut in Makefile to run them, if you want to add a migration just create a new file inside sql with the prefix V(n+1)__ and the name or a description of what your migration will do.
