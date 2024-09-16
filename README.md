# Experimento-gateway

Para ejecutar el gateway desde local usando un ambiente de Docker solo se necesita seguir los siguientes pasos:

## Construir la imagen teniendo habillitad y corriendo el demonio de docker con Docker desktop
        docker build -t gateway .

## Ejecutar el comando para correr el gateway
        docker run --name gateway -p 4000:4000 gateway
