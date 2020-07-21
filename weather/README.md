Structure
------
.  
├── dashboard  # app responsible for live updates  
│  ├── database.py  
│  ├── Dockerfile  
│  ├── main.py  
│  └── requirements.txt  
├── deploy  # deploy suite  
│  ├── dashboard.env  
│  ├── docker-compose.yml  
│  ├── facade.env  
│  ├── nginx_conf  
│  └── postgres.env  
├── facade  
│  ├── Dockerfile  
│  ├── facade  # classic web app  
│  ├── manage.py  
│  ├── requirements.txt  
│  └── weather  
└── README.md  


Deploy
------

Just run `docker-compose up` within `deploy` folder.  
This will build 4 services: database, dashboard, facade and nginx.  
Once you saw facade/sanic startup message, app is fully operational.  
App will be available at [http://localhost:8080](http://localhost:8080).  
Total deployed system takes around ~300mb of data (excluding volumes).  


Createsuperuser
------

Run `docker exec -it <facade container hash> python /app/manage.py createsuperuser`
