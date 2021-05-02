# Centigrade-ChatRoom

 a team project for Build2Learn by [Dharundds](https://github.com/Dharundds), [HrithikMJ](https://github.com/HrithikMJ) & [Zaid](https://github.com/Zaid316)
 

## About

~This a group chatroom application with features like encryption, privacy etc.

~This web application is built using Python's Flask as server side backend and javascript for client side backend and HTML and CSS for frontend.


## Visit

~This web application is hosted using ACI(Azure container instance) [here](http://centigrade-chatroom.southindia.azurecontainer.io:5000/).



~To run the application localy clone this repo and cd into it and run 


`pip install -r requirements.txt`

`export DBSTRING="mongodb://127.0.0.1:27017/"` #Your mongodb string or contact us to get access to our db

`flask run `
        
      

(or) 

~Build the docker image using 

`docker build --tag <NAME> .`

and Run using 

`docker run --name <NAME> -p 5000:5000 --env DBSTRING=<MONGODB_CONNECTION_STRING> <NAME> `




## Host
  
~kindly refer [here](https://github.com/Dharundds/ChatRoom/blob/main/host.md) for detailed info on hosting using heroku.

## Known issues 

~ feel free to report bugs [here](https://github.com/Dharundds/ChatRoom/issues).


## Acknowledgements

~[stackoverflow](https://stackoverflow.com/questions/41804507/h14-error-in-heroku-no-web-processes-running)

~[real-python](https://realpython.com/flask-by-example-part-1-project-setup/) 

~[flask](https://flask-doc.readthedocs.io/en/latest/)
