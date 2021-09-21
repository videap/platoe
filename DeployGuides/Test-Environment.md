# Deploy Test Environment:
The test environment is containerized, prepared for docker, to be run in a test server (test.platoe.io) in Oracle Cloud, with a MySQL database in a different host. The stripe-webhook is configured for the internet on port 80 (http). The orchestration is made to Kubernetes in Oracle Cloud (OKE) using manifests.

It has 2 containers, one proxy (nginx) and one app (django). The build for the image is set in dockerfiles, and they are orchestrated using docker-compose.

Nginx acts as reverse-proxy, presenting the application as web server, and the static and media files in 2 volumes. This volume is shared by the django container, and is set as NFS Server external to the test-server.

Django container has also an application server, that is currently gunicorn.

The most recent code for Test Environment is found inside the test branch. To get it, make sure you have access to platoe repository, and in a working directory, run the commands and populate with your credentials.

```
git clone -b test https://github.com/videap/platoe
```

# Project Structure:

### Django Structure
This project is called plato, and has 1 configured application inside, called ideas. Some configurations are set in the project level, other in the application level.

### Python Packages
They are all defined in the file **requirements.txt**

### Stripe API Keys
The communication with stripe uses API keys for authentication and they must be defined as ENVIRONMENT VARIABLES. You can get the keys with the Admin for the Stripe Account. Below are the variables that must be set:

 - STRIPE_PUBLISHABLE_KEY
 - STRIPE_SECRET_KEY
 - WEBHOOK_SECRET

### Stripe Credit Card for Test
To test payment options, you can use the test card for Stripe, defined by:
  4242 4242 4242 4242

### manage.py
This file is in the root project directory, and is the main file to control django.

### urls.py
The urls file describes all paths for the application. Each path calls for a function inside the views.py, and passes the web request alongside with the defined parameters.
There are 2 urls.py files, the project file, and the application file. The project file is global and is currently configured to include all paths defined in the application urls.py file.


## Components
All components are inside the *idea* folder.

### media/ and media/
This folders is mounted to the container to maintain images and media files. They are served by django in developer environment and configured in the dev-settings.py file. They expose the files found in the MEDIA_ROOT directory using the MEDIA_URL string. For example, a request for plato.io/media/profile_images/user1.png would fetch for an image named user1.png found in the MEDIA_ROOT/profile_mages/ directory.

### static/
This folder holds the CSS and Javascript files, and is also served by django in developer environment. Similar to media, they expose the files found in the STATIC_ROOT directory using the STATIC_URL string

### templates/*.html files

All .html files render the HTML and some javascript code, for each page.

### /static/ideas/react_components.js
All react elements (classes) are defined here, and only that.

### api.py
Defines all functions called by the server or the front-end, mostly to manage data.

### api_stripe.py
Defines functions to interact with stripe. All functions are called by the server side, with information fetched from the database.

### forms.py
Most of the data inserted with POST requests are validated by Django using ModelForms. This file defines the classes used.  

### functions.py
General functions used by views and APIs, such as Paginator and custom validation.

### dockerfiles
There are 2 dockerfiles, 1 in the root directory, and other in the nginx directory, that sits alongside the default.conf file for nginx configuration.

### kubernetes
To orchestrate the deployment, there are manifests inside the k8s/ folder. The environment variables are set in the 

# HOW TO DEPLOY

## 1. Get the code

The most recent code for Test Environment is found inside the test branch. To get it, make sure you have access to platoe repository, and in a working directory, run the commands and populate with your credentials.

```
git clone -b test https://github.com/videap/platoe
```

## 2. Create a virtual environment (for python)
The test server is a Linux OS, Ubuntu distribution. Make sure Python3.8 and virtualenv is installed on the test server running the command:
```
python3 -V
pip3 -V
```
If not, to install python in Ubuntu-18, you need to run these commands:

```
sudo apt install python3
```

To install virtual env, run the command:
```
pip3 install virtualenv
```

To create your virtualenv environment in a folder called "venv" you can run the following command from the directory you want to work. You will access this directory to activate or deactivate the virtual environment:

```
virtualenv venv
```

To activate the virtualenv, run the activate script inside the venv folder. For example, in a terminal, use the command:
```
source venv/bin/activate

```

## 4. Install Docker and Docker-Compose
Check if docker is installed in the test-server, running the command:
```
docker --version
```

If not, docker must be installed in the host. Check [docker documentation](https://docs.docker.com/engine/install/ubuntu/)

Don't forget to add the user to the group that can manage docker. For example, for the user ubuntu:

```
sudo usermod -aG docker ubuntu 
```


It is not necessary to install Docker-Compose with pip, but this enables the usage of ARM arch, freely offered by Oracle Cloud. To install run the commands with the virtual environment activated:

```
pip install docker-compose
```
## 3. Define secrets
The secrets are defined in a yaml file for kubernetes. These defines variables for DB Connection and for Stripe Keys Integration.

There should be a file named secret.yaml (or any file with secret* prefix, for it to be ignored by git) following the template below. Complete the variables accordingly.

```
piVersion: v1
kind: Secret
metadata:
  name: django-secrets
type: opaque
stringData:
  DB_USERNAME: ""
  DB_PASSWORD: ""
  STRIPE_PUBLISHABLE_KEY: ""
  STRIPE_SECRET_KEY: ""
  WEBHOOK_SECRET: ""

```



## 4. Install and connect with kubectl

In a remote server, install the kubectl tool to interact with the OKE cluster. Depending on your host, follow according to this [link](https://kubernetes.io/docs/tasks/tools/). Make sure this host can access the OKE API Endpoint and can authenticate to OCI using the CLI.

To check if your installation is working, run the command in the host for the kubectl tool:
```
kubectl version
```

If everything is set up, to run your containers, you can use the command from the project root directory: 

```
kubectl create -f ./k8s/*
```

To access your application, from any browser, access http://test.platoe.io



