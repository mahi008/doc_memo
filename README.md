## Doc_memo Project progress
- [x] User creation
- [x] User login
- [x] Patient filter
- [x] Predictions
- [x] Tests
- [ ] User authentication before prediction
- [ ] logging
### Requirements :
- Docker

### Setup
1. Clone the repository
2. Once inside project folder, build and execute the project using 

```sh
cd doc_memo
docker-compose build && docker-compose up
```
3. Intialise/import pred defined users
```sh
docker ps # Get the container ID
docker exec -it CONTAINER_ID bash # Enter into the container
python3 import_data.py
```
3. URL's

| Service name          | Url's                                     | Swagger url                |
|-----------------------|-------------------------------------------|----------------------------|
| Users webservice      | http://localhost:5000/                    | http://localhost:5000/docs |
| Prediction webservice | http://localhost:8000/                    | http://localhost:8000/docs |

---

## Usage examples

#### 1. Create a user (Patient, Caregiver or a professional)
**POST** : `http://localhost:5000/user`

**BODY** : 
```sh
################ Patient ################ 
{
    "name": "Johnny",
    "password": "mypassword",
    "status": "patient",
    "age" : 55,
    "memory_score": 45
}
################ Caregiver ################ 
{
    "name": "Johnny",
    "password": "mypassword",
    "status": "caregiver",
    "related_patient": "John"
}
################ Professional ################ 
{
    "name": "Johnny",
    "password": "mypassword",
    "status": "healthcare_professional",
    "type": "general_practitioner"
}
```
---
#### 2. Filter patient by memory score/age (Patient, Caregiver or a professional)
**GET** : `http://localhost:5000/patient`

QUERY PARAMS :

memory score greater than : `mem_score_gt=XX`

age greater than : `age_gt=XX`


age lower than: `age_lt=XX`

**URL EXAMPLES** : 
```sh
################ Memeory score ################ 
http://localhost:5000/patient/?mem_score_gt=15
################ Memeory score and age ################
http://localhost:5000/patient/?mem_score_gt=15&age_gt=30
```
---

#### 3. Get patients predicted score
**GET** : `http://localhost:5000/patient/{XXXXXX}/score`

**PARAMS** :
Patient name/username : `{XXXXXX}=user name`
---

### Project setup detail
To maintain a minimal Docker project, two instances of FastAPI are running within the same project on two different ports. 
This setup simulates two independent microservices

#### Missing features

Due to my personal and professional time constraints, I couldn't finish some features listed below 

1. User authentication before retrieving a prediction score
  
This can be implemented using JWT token, dedicated endpoint which takes username/password,
generates a token with an expiry. Which then can be used upon different requests

2. Logging

Not enough logging, this can be addressed by adding different logs using python logging library.
with different log level `INFO, DEBUG, ERROR, EXCEPTION` etc...