FROM --platform=amd64 docker.io/alpine:3.20
RUN apk -U --no-cache add openjdk21-jre-headless
ADD ./build /server
EXPOSE 25565
WORKDIR /server
ENTRYPOINT ["/bin/sh", "-x", "start.sh"]
