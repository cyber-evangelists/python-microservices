
## Run Locally

Clone the project

```bash
  git clone https://github.com/cyber-evangelists/python-microservices
```

Open in vs code terminal

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  python app.py
```

# How to test

1. Open Postman Http Request Tab

2. Endpoints on local host would be:-

    ###   Add a new User
    ###   POST Request: http://127.0.0.1:5000/users 
    Open Postman select HTTP request, Open Body tab select raw json, insert data like this and send the request
   ```bash

    {
    "name": "Test User",
    "email": "test@example.com"
    }
    ```
  
    ###   Get all users
    ###   GET Request : http://127.0.0.1:5000/users
    Open Postman select HTTP request, Send the request, it will display all users.

    ###   Get a User based on ID
    ###   GET Request : http://127.0.0.1:5000/users/{id}
    Open Postman select HTTP request, Send the request with the id of the user you want to search.
    
    
    ###   Update Username based on ID
    ###   PUT Request http://127.0.0.1:5000/users/{id} 
    Open Postman select HTTP request, Send the request with the id of the user you want to update.
    In raw json send data like this.
     ```bash

    {
    "name": "Test User",
    "email": "test@example.com"
    }
    ```
    ###   Delete a User based on ID
    ###   DELETE Request http://127.0.0.1:5000/users/{id} 
    Open Postman select HTTP request, Send the request with the id of the user you want to delete.

