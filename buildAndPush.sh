docker build -t NAME . --no-cache
docker tag NAME DockerRegistryURL:tag
docker push DockerRegistryURL:tag
