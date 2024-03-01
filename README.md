# Test Google App Engine: Flask app

[Deployment of a Flask app on GCP App Engine](https://cloud.google.com/appengine/docs/standard/python3/building-app?hl=fr)

## Setup your GCP project

### Create a project on GCP

* Create a new project on GCP
* Activate a Billing account

### Install gcloud

* Check if gcloud is installed

  ``` bash
  $ gcloud --version
  ```

  If it is, skip to the next section

* To install glcoud:

  ``` bash
  $ curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-466.0.0-linux-x86_64.tar.gz

  $ tar -xf google-cloud-cli-466.0.0-linux-x86_64.tar.gz

  $ mv google-cloud-sdk /usr/local/lib
  $ cd !$
  $ ./google-cloud-sdk/install.sh

  $ gcloud --version
  ```

* Init gcloud default configuration

  ``` bash
  $ gcloud init
  ```

  List account whose credentials are stored on the local system

  ``` bash
  $ gcloud auth list
  ```

  List the properties of your active configuration

  ``` bash
  $ gcloud config list
  ```

  View the infos of your active configuration

  ``` bash
  $ gcloud info
  ```

## Create a new App Engine app

* List available regions

  ``` bash
  $ gcloud app regions list
  ```

  Once the app created, the region cannot be modified and can have an impact on pricing.  
  [Google Price calculator](https://cloud.google.com/products/calculator)

* Create an app in Belgium

  ``` bash
  $ gcloud app create --region=europe-west
  ```

  View your App Engine details

  ``` bash
  $ gcloud app describe
  ```

## Setup the database

* Activate Cloud Datastore API (the database)

* Create the indexes specified in index.yaml (will take about 5 minutes to be effective)

  ``` bash
  $ gcloud datastore indexes create index.yaml
  ```

## Setup Firebase authentication

* [Add Firebase to your project](https://console.firebase.google.com/?hl=fr)

* Enable Firebase authentication:  
  Authentication > Start > E-mail/password > Save

  Authentication > Authorised domains:  
  add the domain of your app on App Engine without the http:// prefix — ie PROJECT_ID.REGION_ID.r.appspot.com

* Click on the gear next to "project overview"  
  Add a web app

  ![](https://i.imgur.com/8dScor3.png)

* Get the script code snippet

  ![](https://i.imgur.com/ZKKFmAm.png)

* Update templates/index.html with your own credentials

  ``` js
  apiKey: "<API_KEY>",
  authDomain: "<PROJECT_ID>.firebaseapp.com",
  databaseURL: "https://<DATABASE_NAME>.firebaseio.com",
  projectId: "<PROJECT_ID>",
  storageBucket: "<BUCKET>.appspot.com",
  messagingSenderId: "<SENDER_ID>",
  ```

---

## Launch the project

### Locally

* Login to google and create the Application Default Credentials (ADC)

  ``` bash
  $ gcloud auth login --update-adc
  $ ls ~/.config/gcloud/application_default_credentials.json
  ```

* Update the GCLOUD_PROJECT environment variable in docker-compose.yaml

* Launch locally

  ``` bash
  docker-compose up
  ```

  Go to localhost:8080

### On GCP

* Note that app.yaml defines the web app parameters for App Engine

* To deploy (create/update) the app on GCP:

  ``` bash
  $ gcloud app deploy
  ```

* View

  ``` bash
  $ gcloud app browse
  Opening [https://testing-python-415909.ew.r.appspot.com] in a new tab in your default browser.
  ```

* [List App Engine apps](https://console.cloud.google.com/appengine/services?hl=fr)

  [List versions](https://console.cloud.google.com/appengine/versions?hl=fr): on each deploy a new version is created, here you can redirect the traffic to a previous version to rollback the deployment
