# CONTRIBUTING

## How to run the Dockerfile locally

See in [Udemy Flask Telco course ebook](https://rest-apis-flask.teclado.com/docs/deploy_to_render/docker_with_gunicorn/)

teclado-site-flask is the name of the image

To run:

```
docker run -dp 5000:5000 -w /app -v "$(pwd):/app" teclado-site-flask sh -c "flask run --host 0.0.0.0"
```
