# Django template for docker

## Setup

Clone repository

```
docker-compose up -d 
```


For production copy .env.dev to .env.prod and change passwords and keys.
Change trafik labels to fit domain.


## Structure
Configuration is in the top-directory: `settings.py`, `urls.py`

docker-compose.prod.yml is prepared for use with the traefik load balancer.
