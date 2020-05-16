# Django template for docker

## Setup

Clone repository

```
docker-compose up -d 
```

## Deployment

```
docker-compose -f docker-compose.prod.yml up -d
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```


For production copy .env.dev to .env.prod and change passwords and keys.
Change trafik labels to fit domain.


## Structure
Configuration is in the top-directory: `settings.py`, `urls.py`

docker-compose.prod.yml is prepared for use with the traefik load balancer.


