[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-f059dc9a6f8d3a56e377f745f24479a46679e63a5d9fe6f495e02850cd0d8118.svg)](https://classroom.github.com/online_ide?assignment_repo_id=7091320&assignment_repo_type=AssignmentRepo)
# Data Affairs

This repository is created for the CMPT 756 Course Project. It contains the code to develop and test microservices in Google Cloud Environment. 

## Setting up the project...

### Initialize the Template File

Create a tpl-vars.txt file using the tpl-vars-blank.txt in the same directory as reference and fill in the details asked for inside the file. This ensures the aws and github credentials. 


### Instantiate every template file using this command:

`make -f k8s-tpl.mak templates`


### The Google Cloud Platform 

For our project, we have chosen Google Cloud Platform as the PAAS for deploying our application. 

-> Install Google Cloud SDk on the local machine using:
-> Instantiate gcloud on local machine, set the region, select the project and further details if prompted.
-> Finally you can start the cluster by going to project root directory and using command:

`make -f gcp.mak start `

#### Create a namespace: 

`kubectl config use-context gcp756  `

`kubectl create ns c756ns`  

`kubectl config set-context gcp756 --namespace=c756ns `



### Installing required packages

#### Installing service mesh and istio:  

`kubectl config use-context gcp756 `

`istioctl install -y --set profile=demo --set hub=gcr.io/istio-release `

`kubectl label namespace c756ns istio-injection=enabled `


### Building the image

#### Build your images and push to ghcr 

`make -f k8s.mak cri `
 
#### To force build your images and push to ghcr 

`make -B -f k8s.mak cri `


### Deploying the services

Once all the changes have been made and services are ready to be deployed, use the following command to deploy them:

`make -f k8s.mak gw db s1 s2 s3`

Or use the following command to ensure that metrics and observation services are deployed along with the microservices:

`make -f k8s.mak provision`  
#### Get the URL for the microservice deployed:

`kubectl -n istio-system get service istio-ingressgateway | cut -c -140`

### Get the URL for the metric services running

#### Checking grafana url: 

`make -f k8s.mak grafana-url `
 
#### Checking prometheus url: 

`make -f k8s.mak prometheus-url `

#### Checking kiali url: 

`make -f k8s.mak kiali-url` 
 
 
### Checking the logs of each service: 

In case of errors or to check the history, use the following command to view logs:

`kubectl logs --selector app='service_name' --container 'service_name' --tail=-1` 

Or can be viewed from k9s.


## Scaling

To Scale a particular service use the following command:

`kubectl scale deploy/'service_name' --replicas='number_of_replicas'`

Example: Scale the application db services to 3 replicas: 

`kubectl scale deploy/cmpt756db --replicas=3 `

And to check if it has been reflected: 

`kubectl describe deploy/cmpt756db `


