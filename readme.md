
To activate the environment: 
source venv/bin/activate

To test the python setup scripts:
On local, docker app must be running ;) . This should run the kubernetes cluster
Refer to readme on elasticsearch repository (see port forwarding below, which is not persistent), and check the connection with Thunder client:
kubectl port-forward deployment/elasticsearch 9200:9200

Elastic search pod must be running

export ELASTIC_USER=...
export ELASTIC_PASSWORD="..."

# Build 
docker desktop must be running ;)

docker login -u your-dockerhub-user. (need to type the password)
docker build -t your-dockerhub-user/my-private-repo:python-indexation-x.y .

to check what is inside:
docker run --rm -it your-dockerhub-user/my-private-repo:python-indexation-x.y /bin/bash

kubectl create secret docker-registry regcred \
  --docker-server=https://index.docker.io/v1/ \
  --docker-username=your_docker_username \
  --docker-password=your_docker_password_or_token \
  --docker-email=your_email

kubectl get secrets

docker push your-dockerhub-user/my-private-repo:python-indexation-x.y
image in deployment.yaml must have the right version!

(if necessary:
kubectl get jobs
kubectl delete job es-init-index)


kubectl apply -f deployment/create_index.yaml

kubectl apply -f deployment/deployment.yaml



#TODO: transform check_settings in python and integrate in create index deployment, try create index deployment
+ now version is 1.4

kubectl get pods

kubectl logs <pod-name>

