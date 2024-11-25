# CRUD Blog App with Fastapi and MongoDB

- [CRUD Blog App with Fastapi and MongoDB](#crud-blog-app-with-fastapi-and-mongodb)
  - [Introduction](#introduction)
  - [Prerequisite](#prerequisite)
  - [Folder Structure](#folder-structure)
  - [Installation](#installation)
  - [Database](#database)
  - [Authentication](#authentication)
  - [Docker](#docker)


## Introduction
This is is a blogging web application where users can register and then login using JWT authentication. Then create,read,update or delete blogs.

## Prerequisite

- Python 3.12
- Local MongoDb server
  

## Folder Structure

```paintext
blog-project/
├── env/                    # Virtual environment folder 
├── blog_app/               # Main application module
│   ├── users/              # Submodule for user management
│   │   ├── models.py       # User-related database schema
│   │   ├── routes.py       # User-related API routes
│   │   ├── schemas.py      # Pydantic schemas for user data validation
│   │   ├── dependencies.py # Used to get the current logged in user
│   ├── posts/              # Submodule for post management
│   │   ├── models.py       # Post-related database schema
│   │   ├── routes.py       # Post-related API routes
│   │   ├── schemas.py      # Pydantic schemas for post data validation
├── .env                    # Environment variables file
├── database.py             # Database connection setup
├── main.py                 # Entry point for the FastAPI application
├── Dockerfile              # Dockerfile for containerization
├── requirements.txt        # Dependencies for the project
```



## Installation

 
- **Clone the repository**  
   Clone the project repository to your local machine:
   ```bash
   git clone https://github.com/EvilMorty13/CRUD_BLOG_FASTAPI.git
   cd CRUD_BLOG_FASTAPI
   ```
 
- **Create and Activate virtual enviroment**

   ```bash
   python3 -m venv env
   source env/bin/activate
   ```
- **Install Requirements**
    ```bash
    pip install -r requirements.txt
   ```


## Running the Project

- **Start The server**
    ```bash
   uvicorn main:app --reload
   ```

- **Access The server**
    ```bash
   http://127.0.0.1:8000/
   ```

- **Explore Api Documentation**
    ```bash
   http://127.0.0.1:8000/docs
   ```

## Database
Create a cluster in your local Mongodb server and then edit the database.py file

- **database.py**
    ```bash
    client = MongoClient("mongodb://localhost:27017/")
   db = client["database name"]
   ```

## API Endpoints

### User Endpoints

- **User registration[POST]**
    ```bash
   http://127.0.0.1:8000/users/register
   ```
- **User Login[POST]**
    ```bash
   http://127.0.0.1:8000/users/login
   ```

### Post Endpoints

- **Create Post[POST]**
    ```bash
   http://127.0.0.1:8000/posts/
   ```
- **Get All Post[GET]**
    ```bash
   http://127.0.0.1:8000/posts/
   ```
- **Update Post[PUT]**
    ```bash
   http://127.0.0.1:8000/posts/{post_id}
   ```
- **Delete Post[DELETE]**
    ```bash
   http://127.0.0.1:8000/posts/{post_id}
   ```
- **Get Posts of current user[GET]**
    ```bash
   http://127.0.0.1:8000/posts/my_posts
   ```

## Authentication
After login, a acces token will be generated.
   The lifetime of that token is 30 minutes. Use the access token to do things like posting,updating and deleting a blog.

- **Using Token**
    ```bash
   Authentication : Bearer <Access Token>
   ```

## Enviroment Variables 
Secret, Algorithm and Token lifetime are hidden using .env file. Make sure to add that in the project.

- **.env**
    ```bash
   SECRET_KEY = "my_key"
   ALGORITHM = "my_algo"
   ACCESS_TOKEN_EXPIRE_MINUTES = 10  
   ```

## Docker

- **Create an Image**
    ```bash
   sudo docker build -t blog-fastapi .
   ```

- **List of Images**
    ```bash
   sudo docker images
   ```

- **Run the Docker Container**
    ```bash
   sudo docker run -d -p 8000:8000 blog-fastapi
   ```

- **Run docker container using host network**
   ```bash
   sudo docker run --network host -d -p 8000:8000 blog-fastapi
   ```

- **List of Containers**
    ```bash
   sudo docker ps
   ```

- **Stop the Docker container**
    ```bash
   sudo docker stop <container_id>
   ```

- **Save an image**
    ```bash
   sudo docker save -o blog-fastapi.tar blog-fastapi
   ```

- **ID of exited containers**
    ```bash
   sudo docker ps -a
   ```

- **Container Logs**
   ```bash
   sudo docker logs <container_id>
   ```

- **Remove a Container**
   ```bash
   sudo docker rm <container_id>
   ```

- **Remove an Image**
   ```bash
   sudo docker rmi <imgae_id>
   ```




