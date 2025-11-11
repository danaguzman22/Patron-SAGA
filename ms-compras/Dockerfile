FROM openjdk:21-jdk-slim

WORKDIR /app

# Copia el archivo .jar sin importar su nombre exacto
ARG JAR_FILE=build/libs/*.jar
COPY ${JAR_FILE} app.jar

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "app.jar"]

