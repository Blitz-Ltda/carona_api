
### Project Setup Instructions
1. **Clone the Repository**
   ```bash
   git clone git@github.com:Blitz-Ltda/carona_api.git

    cd carona_api
   ```

2. **Setup .env**
    Make sure you have a `.env` file in the root directory. You can create it by copying the example file:
    ```bash
    cp .env.example .env
    ```
3. **Install Docker and Docker Compose**
   Ensure you have Docker and Docker Compose installed on your machine. You can download them from the official Docker website.

4. **Build and Start the Containers**
    Run the following command to build the Docker images and start the containers:
    ```bash
    docker-compose up -d --build
    ```

5. **Run Database Migrations**
    After the containers are up, run the database migrations using Alembic:
    ```bash
    docker-compose exec web alembic upgrade head
    ```

6. **Check Logs**
    You can check the logs of the web service to ensure everything is running smoothly:
    ```bash
    docker-compose logs web
    docker-compose logs db
    ```

7. **Access the Application**
    Open your web browser and navigate to `http://0.0.0.0:3000/docs` to access the application.

8. **Stopping the Application**
    To stop the application, you can run:
    ```bash
    docker-compose down
    ```

9. **Running Tests**
    To run the tests, you can execute:
    ```bash
    docker-compose exec web pytest
    ```

10. **Accessing the Database**
    You can access the PostgreSQL database using a database client or through the command line:
    ```bash
    docker-compose exec db psql -U postgres
    ```

### Additional Notes
- Ensure that you have the necessary permissions to run Docker commands.
- If you encounter any issues, check the logs for errors and ensure that your `.env` file is correctly configured.
- For development purposes, you can modify the code in the `app` directory, and the changes will be reflected immediately due to the volume mapping in Docker Compose.
- If you need to add new dependencies, you can modify the `requirements.txt` file and rebuild the Docker image using:
    ```bash
    docker-compose up -d --build
    ```
- For more advanced configurations, refer to the Docker and Docker Compose documentation.

### Project Overview
This project is a RESTful API built with FastAPI, designed to manage carpooling (carona) services. It uses PostgreSQL as the database and includes features such as user authentication, ride management, and more.

### Project Structure
```
.
├── app
│   ├── api
│   ├── models
│   ├── repositories
│   ├── schemas
│   ├── services
│   ├── shared
│   └── main.py
├── .env.example
├── .gitignore
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── README.md
├── requirements.txt
├── alembic/
├── tests/
