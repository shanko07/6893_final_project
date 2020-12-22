1. run `docker build -t 6893predapp:v1 .`
2. run `docker run -d -p 127.0.0.1:8457:5000 --restart unless-stopped 6893predapp:v1`
