
# Build 
docker desktop must be running ;)


docker login -u your-dockerhub-user. (need to type the password)
docker build -t your-dockerhub-user/my-private-repo:python-indexation-x.y .

docker run --rm -it your-dockerhub-user/my-private-repo:python-indexation-x.y /bin/bash

kubectl create secret docker-registry regcred \
  --docker-server=https://index.docker.io/v1/ \
  --docker-username=your_docker_username \
  --docker-password=your_docker_password_or_token \
  --docker-email=your_email

kubectl get secrets

docker push your-dockerhub-user/my-private-repo:python-indexation-x.y
image in deployment.yaml must have the right version!
kubectl apply -f deployment/deployment.yaml

kubectl get pods

kubectl logs <pod-name>

