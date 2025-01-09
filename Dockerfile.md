# 构建镜像
docker build -t xiaomi-observer:v1 .

# 运行容器
docker run -d --name xiaomi-observer \
-e LONGPORT_APP_KEY= \ 
-e LONGPORT_APP_SECRET= \ 
-e LONGPORT_ACCESS_TOKEN= \
-e QQ_EMAIL= \
-e QQ_EMAIL_AUTHORIZATION_CODE= \
xiaomi-observer:v1

# 登录docker
docker login

# 标记镜像
docker tag xiaomi-observer:v1 username/xiaomi-observer:v1

# 推送镜像
docker push username/xiaomi-observer:v1