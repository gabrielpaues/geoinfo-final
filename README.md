# geoinfo
Geoinfo demo for Kubernetes

Input your variables in the plotvars.py file.

Build and start the container:
# sudo docker build --tag=geoinfo-0.1 . && sudo docker run -p 4000:80 geoinfo-0.1

Then surf to localhost:4000/plot to see the map.

Run the container and then connect to localhost:4000/plot to get a map showing where the running container is in the world.
