Este es el archivo de configuración de la API creada para la resolución del desafio técnico. Esta misma se uso con Flask y se hizo el despligue a través de la
plataforma Render. El enlace donde se implemento la API es https://flask-api-sah3.onrender.com/

Para el uso de la misma se debe llamar al endpoint /mutant a través del metodo POST con un cuerpo con la siguiente estructura:

{"dna": ["ATGCGT", "AAGTGT", "ATGATT", "AGATGT", "GCGTAA", "TCACTT"]}'

Si se clona este repositorio, se puede llamar desde la terminal local de su dispositivo al archivo de Python "api_example_usage.py", donde se utiliza la
libreria request con el fin de llamar al endpoint dada la secuencia ADN que verifica si es o no un mutante.

Los datos se guardan en una base de datos de PostgreSQL que se puede acceder a las métricas pedidas en el Nivel 3 del enunciado de esta desafio técnico
a través del endpoint /stats
