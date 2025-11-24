# Etapa 1: Compilar el proyecto usando Gradle + JDK
FROM gradle:8.5-jdk21 AS build
WORKDIR /home/gradle/project
COPY . .
RUN gradle build --no-daemon

# Etapa 2: Imagen final liviana para correr el .jar
FROM eclipse-temurin:21-jdk-jammy
WORKDIR /app
COPY --from=build /home/gradle/project/build/libs/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
