# ukcodes

Es una implementación de consumidor de API, orientado a la escalabilidad y la resiliencia. Consta de dos micro-servicios, a saber: un endpoint web y un consumidor accesible por colas de RabbitMQ.

Su ciclo de ejecución es el siguiente:

1. El usuario sube un archivo CSV a el “endpoint” (/ukcodes/upload), el sistema lo recibe, verifica que el tipo de contenido del fichero sea CSV; si es así devuelve un id de tarea (task_id) el cual puede ser usado en diferido para consultar el estado del análisis del archivo en la ruta (/ukcodes/{task_id}), sino devuelve un mensaje de error 415, de tipo de medio no soportado.

2. El “endpoint” crea una tarea de “análisis de fichero”, que comprueba la integridad del formato CSV, verifica que los valores de cada linea sean congruentes con coordenadas geográficas, filtra la lineas en blanco y las lineas con datos repetidos. Una vez terminado el proceso, se crea una tarea de “envío de coordenadas” la cual se realiza mediante una cola de RabbitMQ con destino al micro servicio “consumidor”. El envió se realiza en forma de lista de texto, de máximo 100 elementos por paquete.

3. El “consumidor” escucha la cola de mensajes conectada a la tarea de “envió de coordenadas”, cuando recibe un paquete, evaluá cada elemento contra una cache de eliminación almacenada en REDIS, de esta forma garantiza que no se consulte mas de una vez la misma coordenada.

4. Los elementos del paquete que no son descartados por la cache de eliminación, se usan para formar un cuerpo de consulta json compatible con la acción “Bulk Reverse Geocoding” del API de postcodes.io (api.postcodes.io/postcodes). Se usa el siguiente formato, con un máximo de 100 elementos:

{
  "geolocations" : [{
    "longitude":  0.629834723775309,
    "latitude": 51.7923246977375,
    "limit": 1
  }, {
    "longitude": -2.49690382054704,
    "latitude": 53.5351312861402,
    "limit": 1
  }]
}

5. Se utiliza la librería REQUESTS para hacer la consulta POST al API y luego se verifican los resultados de cada coordenada, para eliminar aquellas que den un resultado nulo. La respuesta tiene la siguiente forma:

{
    "status": 200,
    "result": [
        {
            "query": {
                "longitude": "0.629834723775309",
                "latitude": "51.7923246977375",
                "limit": "1"
            },
            "result": [
                {
                    "postcode": "CM8 1EF",
                    "quality": 1,
                    "eastings": 581459,
                    "northings": 213679,
                    "country": "England",
                    "nhs_ha": "East of England",
                    "longitude": 0.629806,
                    "latitude": 51.792326,
                    "european_electoral_region": "Eastern",
                    "primary_care_trust": "Mid Essex",
                    "region": "East of England",
                    "lsoa": "Braintree 017F",
                    "msoa": "Braintree 017",
                    "incode": "1EF",
                    "outcode": "CM8",
                    "parliamentary_constituency": "Witham",
                    "admin_district": "Braintree",
                    "parish": "Witham",
                    "admin_county": "Essex",
                    "admin_ward": "Witham South",
                    "ced": "Witham Southern",
                    "ccg": "NHS Mid Essex",
                    "nuts": "Essex Haven Gateway",
                    "codes": {
                        "admin_district": "E07000067",
                        "admin_county": "E10000012",
                        "admin_ward": "E05010388",
                        "parish": "E04012935",
                        "parliamentary_constituency": "E14001045",
                        "ccg": "E38000106",
                        "ccg_id": "06Q",
                        "ced": "E58000470",
                        "nuts": "TLH34",
                        "lsoa": "E01033460",
                        "msoa": "E02004462",
                        "lau2": "E07000067"
                    },
                    "distance": 1.98709706
                }
            ]
        }
    ]
}

6. Las coordenadas que han generado una respuesta valida, son enviadas mediante un broker RabbitMQ a un worker en segundo plano, el cual abre una conexión a base de datos por cada conjunto de datos validos (entre 1 y 100 coordenadas). La información se almacena en tres tablas simples, a saber: Una con la lista de coordenadas (coordinate), una con los datos principales de cada código postal vinculado a su coordenada (postcode) y una con los códigos seriales de cada código postal (codes).
Dado que el usuario puede subir archivos realmente grandes y que la consulta efectiva al API de postcodes.io es efectivamente un cuello de botella; se opto por una arquitectura que mantuviera todos los procesos “lentos” en segundo plano, permitiendo dar una respuesta rápida al usuario, y manteniendo un flujo de trabajo fácilmente escalable.

El siguiente diagrama ilustra conceptual mente el diseño interno del sistema: 

![alt text](https://github.com/ejherran/ukcodes/blob/main/img/arq.png?raw=true)


# EJECUCIÓN:

Para poner en marcha el sistema basta con ejecutar el comando:

docker-compose up -d –build 

Estando en el directorio principal del proyecto. Se recomienda el uso de docker-compose integrado como plugin de docker y con una versión igual o superior a 2.2.0.

El fichero “env_vars” contiene las variables de entorno que se usan para configurar todos usuarios y permisos de los contenedores. La información persistente se almacena en el directorio “.env/” que se crea con la primera ejecución del sistema.

Puede usar el comando docker logs -f [container] para ver en primer plano los mensajes de ejecución tanto de los servicios, como de los workers. De igual forma puede usar el comando docker exec -it [mariadb-container] bash para acceder al interior del contenedor y usar el cliente mysql para ver los datos almacenados.

Para consumir el “endpoint” se recomienda el uso de PostMan, como si ilustra a continuación.

![alt text](https://github.com/ejherran/ukcodes/blob/main/img/post.png?raw=true)

![alt text](https://github.com/ejherran/ukcodes/blob/main/img/get.png?raw=true)

Para conocer el razonamiento detrás de esta “abominación” consulte el archivo argument.txt