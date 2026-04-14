
# To activate the environment: 
source venv/bin/activate

# To test the python setup scripts:
On local, docker app must be running ;) . This should run the kubernetes cluster
Refer to readme on elasticsearch repository (see port forwarding below, which is not persistent), and check the connection with Thunder client.
Once ok, forward the port:
kubectl port-forward deployment/elasticsearch 9200:9200

Elastic search pod must be running
Setup the elastic password from keypass:
export ELASTIC_PASSWORD="..."
Note:
- ELASTICSEARCH_URL : no need to set, default is http://localhost:9200
- ELASTIC_USER : no need to set, default is elastic

# Build 
docker desktop must be running ;)

docker login -u your-dockerhub-user (need to type the password)
docker build -t your-dockerhub-user/my-private-repo:python-indexation-x.y .


to check what is inside:
# docker run --rm -it your-dockerhub-user/my-private-repo:python-indexation-x.y /bin/bash
current:1.16


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
kubectl delete job es-init-index
kubectl delete job es-check-index
kubectl delete job es-scrap-website
kubectl delete job es-check-scrapping
kubectl delete job es-delete-index

#to redo
kubectl apply -f kubernetes/delete_index.yaml

kubectl apply -f kubernetes/create_index.yaml
kubectl apply -f kubernetes/index_check.yaml
kubectl apply -f kubernetes/scrap_my_website.yaml
kubectl apply -f kubernetes/verify_scrapping.yaml
kubectl get pods
Check for the pod name starting with es-check-index-
kubectl logs <pod-name>
# To test with Thunder client, do not forget about port forwarding if you have not done it before
kubectl port-forward deployment/elasticsearch 9200:9200


#TODO: transform check_settings in python and integrate in create index deployment, try create index deployment
+ now version is 1.4

kubectl get pods

kubectl logs <pod-name>

To check interactively inside the image of the python environment:
kubectl apply -f deployment/python_debug_environment.yaml
kubectl exec -it <pod-name> -- /bin/bash

# Beware that the node search api is caching queries. You may need to restart the server kubectl delete pod nodeapp-....
ollama run phi3:mini

# Run all tests to get the coverage. Results on htmlconv (conversion is not well calculated when running the tests from the test menu on vs code)
# You must install the Live Server extension to view the index.html in the htmlconv folder
# You can also add the extension coverage gutter to see the coverage directly from your code
pytest --cov=src \
       --cov-report=term-missing \
       --cov-report=html \
       --cov-report=xml

