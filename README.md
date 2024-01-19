# deep-authentication-app

The goal of the project is to create a face authentication system that can be installed in places where high security is required.
This is a modern Face Authentication System which includes state-of-art algorithms to detect face and generate face embedding. This system contains endpoints which can be integrated to any device depending on the requirements. The ayatem has 2 stage authentication system
ie manual using login id and password and face based authentication system using MTCNN and FaceNet.

## Tech Used
1. MTCNN,FaceNet
2. Fast API
3. Mongo DB
4. Azure Container Registry,Azure App Service

## Project Architechture
<img width="844" alt="image" src="https://user-images.githubusercontent.com/57321948/195135349-9888d9ea-af5d-4ee2-8aa4-1e57342add05.png">

## Run the Application
The project uses MongoDB with Compass for data storage.Azure is used to access the service like ACS and App services.

### Step 1-: Clone the Repository
```
git clone https://github.com/Deep-Learning-01/Deep-Authenticator.git
```

### Step 2-: Create conda environment
```
conda create -p ./env python=3.8.13 -y
```

### Step 3-: Activate Conda environment
```
conda activate ./env
```

### Step 4-: Install requirements
```
pip install -r requirements.txt
```

### Step 5-: Export the environment variable
```
export SECRET_KEY=<SECRET_KEY>

export ALGORITHM=<ALGORITHM>

export MONGODB_URL_KEY=<MONGODB_URL_KEY>

export DATABASE_NAME=<DATABASE_NAME>

export USER_COLLECTION_NAME=<USER_COLLECTION_NAME>

export EMBEDDING_COLLECTION_NAME=<EMBEDDING_COLLECTION_NAME>
```
### .env file
```
SECRET_KEY=KlgH6AzYDeZeGwD288to79I3vTHT8wp7
ALGORITHM=HS256
DATABASE_NAME='UserDatabase'
USER_COLLECTION_NAME='User'
EMBEDDING_COLLECTION_NAME='Embedding'
MONGODB_URL_KEY=
```

### Step 6-: Run the application server
```
python app.py
```

## Run Locally

### Build the Docker Image
```
docker build -t face_auth --build-arg SECRET_KEY=<SECRET_KEY> --build-arg ALGORITHM=<ALGORITHM> --build-arg MONGODB_URL_KEY=<MONGODB_URL_KEY> --build-arg DATABASE_NAME=<DATABASE_NAME> --build-arg USER_COLLECTION_NAME=<USER_COLLECTION_NAME> --build-arg EMBEDDING_COLLECTION_NAME=<EMBEDDING_COLLECTION_NAME> . 
```

### Run the Docker Image

```
docker run -d -p 8000:8000 <IMAGEID OR IMAGENAME>
```
## Deployment to Azure

### Services used
- Azure container Registry (ACR) for Docker image of project is stored
- Azure App Services for deploying the application
- GitHub Actions for CI/CD


