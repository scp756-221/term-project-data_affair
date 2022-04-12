[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-f059dc9a6f8d3a56e377f745f24479a46679e63a5d9fe6f495e02850cd0d8118.svg)](https://classroom.github.com/online_ide?assignment_repo_id=7091320&assignment_repo_type=AssignmentRepo)
# Data Affair CMPT 756 project

This repository is created for the CMPT 756 Course Project. It contains the code to develop and test microservices in Google Cloud Environment. 

## Setting up the project...

### Prerequisites

1. For our project, we have chosen Google Cloud Platform as the PAAS for deploying our application. Install [Google Cloud SDk](https://cloud.google.com/sdk/docs/install) on the local machine and set the region, select the project and further details if prompted.
2. Download and install [istioctl](https://istio.io/latest/docs/setup/getting-started/#download).
3. Install [helm](https://helm.sh/docs/helm/helm_install/).

### Initialize the Template File

Create a tpl-vars.txt file using the tpl-vars-blank.txt in the same directory as reference and fill in the details asked for inside the file. This ensures the aws and github credentials. 


### Instantiate every template file using this command:

`make -f k8s-tpl.mak templates`

### Starting cluster:
Finally you can start the cluster by going to project root directory and using command:

`make -f gcp.mak start`

This will also make kubectl use context to gcp756, create a namespace c756ns and set the context to gcp756 for the created namespace c756ns.

### Building the image

#### Build your images and push to ghcr 

`make -f k8s.mak cri `
 
#### To force build your images and push to ghcr 

`make -B -f k8s.mak cri `


### Deploying the services

Use the following command to ensure that metrics and observation services are deployed along with the microservices:

`make -f k8s.mak provision`  

This command will also install service mesh and istio and enable istio injection. In addition, it will also run the cloudformation stack to create DynamoDB tables and loader to initialize data in the DynamoDB tables.

#### Get the URL for the microservice deployed:

`kubectl -n istio-system get service istio-ingressgateway | cut -c -140`

### Testing the API calls:

#### Create purchase:

`IGW=<URL> BODY_PURCHASE=<BODY> make -e -f api.mak cpurchase`

Replace IGW with the url obtained from the previous command to paste here.

Example:
`IGW=34.83.42.29 BODY_PURCHASE='{ "music_id":"1", "user_id":"1", "purchase_amount":"50" }' make -e -f api.mak cpurchase`
Respone:
`{"purchase_id":"d416ab13-53ec-4a30-8585-39f46fb21166"}`
#### Read purchase:

`IGW=<URL> PURCHASE_ID=<PURCHASE_ID> make -e -f api.mak rpurchase`

Example:
`IGW=34.83.42.29 PURCHASE_ID=d416ab13-53ec-4a30-8585-39f46fb21166 make -e -f api.mak rpurchase`

#### Delete Purchase:
`IGW=<URL> PURCHASE_ID2=<PURCHASE_ID> make -e -f api.mak dpurchase`

Example:
`IGW=34.83.42.29 PURCHASE_ID2=d416ab13-53ec-4a30-8585-39f46fb21166 make -e -f api.mak dpurchase`

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


## Failure Simulations

To simulate various failure scenarios, we can use the following commands:

1. Canary deployment:
`kubectl -n c756ns apply -f cluster/s3-vs-v1.yaml`
2. Circuit breaker:
`kubectl -n c756ns apply -f cluster/s3-vs-circuitbreaker.yaml`
3. Delay injecion:
`kubectl -n c756ns apply -f cluster/db-vs-delay.yaml` -> to set fixed delay to 10s
`kubectl -n c756ns apply -f cluster/s3-vs-delay.yaml` -> to introduce timeout to 2s

