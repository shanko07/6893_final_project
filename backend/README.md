1. move up one directory
2. add Model_D50_N25/whole_dataset.joblib and Model_D50_N25/model_cols to the models directory (they are too big to store in github)
3. run `docker build -t 6893app:v1 -f Dockerfile_Backend .`
4. run `docker run -d -p 127.0.0.1:8456:5000 --restart unless-stopped 6893app:v1`
