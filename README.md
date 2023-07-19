# SiemensNLP
### Siemenes Technical Assesment - Pablo Saucedo

## Requirements
To execute the PoC, only the following is required:
- Docker
- Docker-compose

## Execution
From the home directory, run:
```docker-compose up```

## Data
The data is loaded into the solution from the UI, which will then load it into Mongo.
The */data* folder is left in order to have the data in an accessible way. The original dataset **"reviews.txt"**
takes too long to be processed. That is why we have prepared a reduced version **"small_reviews.txt"**
that allows to use the application in reasonable times.