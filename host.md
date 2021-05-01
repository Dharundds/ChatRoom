# HOW TO HOST ON HEROKU

## pre requisite
`sudo apt install python3`
`mkdir filename`
`cd filename`
replace "filename" with a name of your choice.

installing heroku-CLI
`curl https://cli-assets.heroku.com/install.sh | sh` 

	
## V-ENV
creating a virtual environment
`python3 -m venv venvname`
replace "venvname" with a name of your choice.

### activating venv
`source venv/bin/activate`

## creating app

`paste your app and its files in "venvname" folder`
```
example-app/
	│		     				
	├── venvname/       
	├── templates/       `
	├── static/         
	├── db.py           
	├── user.py	    
	├── app.py	    		
	└── requirements.txt
```
run flask to test your code

`flask run`

### creatig dependecies
 ` pip3 install gunicorn==20.0.4`
 
#### creating requirements.txt

 `pip3 freeze > requirements.txt`
 
#### Creating procfile 
 
 `echo "web gunicorn app:app" > Procfile`
 
#### Creating heroku.yml

 `touch heroku.yml` 
  
  open the file and copy the following code
  
  ```docker
 build:
  docker:
    web: Dockerfile
run:
  web: uvicorn main:app --reload --host 0.0.0.0 --port $PORT
  ```
  
refer [here](https://stackoverflow.com/a/66258772) for explanation.  
 
## adding git

```
  git init
  echo venv > .gitignore
  echo __pycache__ >> .gitignore
  git add .gitignore app.py requirements.txt templates Procfile heroku.yml static db.py user.py
  git commit -m "message"
``` 
    	 
## heroku
 

 `heroku login`
 `heroku create appname`
  replace "appname" with name of yout choice.
  
### pushing to master
 
 `git push heroku master`
 
 `heroku ps:scale web=1`
 
 
## acknowledments

[stackoverflow](https://stackoverflow.com/questions/41804507/h14-error-in-heroku-no-web-processes-running)

[real-python](https://realpython.com/flask-by-example-part-1-project-setup/) 
	
