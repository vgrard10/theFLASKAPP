# Last session project.
## Duration: 3h

# Brief description

This is an overly simplistic application developped using the Flask micro web-framework. 
Of course you can do better in terms of code refactoring (especially the app.py file), but that's not the main focus here. 
It uses an already trained (logistic regression) model to predict if the user would have had survived to the Titanic, given the data he submits to the server.
It also caches the predictions and inputs in a Postgres database so that a user may only submit its details once (can't retry a prediction with the same username).

<u>What we ask you to do is:</u>
1. **containerize this app**, bundling it along with its dependencies using a **Dockerfile** 
2. **orchestrate it** using a **docker-compose.yml file**, with a **Postgres server** using the corresponding **Docker image** from the Docker Hub registry.

# Prerequities

1. You **must** have a GitHub account.
2. **Fork** this repository.
3. Git **clone** the **forked** repository into a local repository: `git clone your_forked_repo_https_url`
4. PLay with the app, read the code
5. Create a **Dockerfile + docker-compose.yml** file
6. Check if your containerized app works\*
7. Git push\*
8. Post your name, lastname (as appears on the DVO/attendance list) and Github link here: https://forms.gle/qhdQQ2mcgPenCgdb7

# Must do !
- Dockerfile and docker-compose.yml file should be in **root project folder**.
- the service name for the flask application in the docker-compose file **must** be named ***flaskapp***.
- I must be able to run your project only by doing `docker-compose up --build`, no more!
- In the dockerfile, you must copy the whole content of the flaskapp folder in a dedicated folder in the container.
- The Python code **MUST NOT** be modified, **NOR** moved under **NO** circumstances, **only 1 Dockerfile and 1 docker-compose file should be created**

Anything that does not respect the aforementioned conditions will result in an automatic score of 0 for this exam. This is CRUCIAL so that I can perform the tests on your project.

\* How to push code,
Do your modifications, and at the end of the 3h session, from your **root project folder**, do from your terminal:
```sh
	git add .
	git commit -m "first commit"
	git push origin master
```

To install git on your [computer](https://git-scm.com/book/fr/v2/Démarrage-rapide-Installation-de-Git)
in [english](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

## Tips

1. Include this block in your Dockerfile
```
	RUN wget https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh -P /scripts
	RUN chmod +x /scripts/wait-for-it.sh
	ENTRYPOINT ["/scripts/wait-for-it.sh", "db:5432", "--"]
```
2. Running the app can be done simply `python app.py runserver --host=0.0.0.0 --threaded`. This should then also be the **Dockerfile default startup command**.
3. Look at the whole project (code, config file, etc.) to check the dependencies to install, name of the service to give, and env variables to be set.