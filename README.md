# Sales-Insight: Prueba técnica para Tía.

<div align="center"><img src="https://i.imgur.com/hsNYjhJ.png" alt="logo.png" width=150></div>

Este proyecto tiene el proposito de demostrar mis habilidades y conocimientos en la parte del desarrollo WEB, Backend y SQL puro. Cómo problema inicial se nos da un set de datos el cuál debemos de llevarlo a una base de datos propia y con ello manipularlo en base a los requerimientos que se piden.

## Requerimientos (Frontend):

- Debe de existir una función para filtrar datos (Ciudad, Estado, Fecha...)
- 2 Tablas en total (Mejores 10 clientes y mejores 20 productos)
- 2 Gráficos a mostrar como mínimo (Fecha VS Tiempo y las ventas por categorías)
- Reponsive design
- 2 Indicadores cómo mínimo (Total de ventas y ventas por segmento)

## Herramientas Usadas
Este proyecto fue realizado con las siguientes herramientas:

### Frontend
- HTML, CSS y JS puro
- Vite para la instalación de librerias
- Tailwind para un CSS más rápido
- ChartJS para crear los gráficos
### Backend
- DJango para crear la API Rest
- PostgreSQL
### Adicional
- Dataset previamente creado ([link aquí](https://www.kaggle.com/datasets/bhanupratapbiswas/superstore-sales?select=superstore_final_dataset+%281%29.csv))
- Excalidraw para hacer borradores de diseños
- Postman para probar endpoints de tipo POST

## Descarga e Instalación

Para poder descargar e instalar este proyecto es muy importante que tengas instalado **Node** para instalar los paquetes y correrlos de manera correcta.

Primero deberás abrir un CMD o Powershell y te deberás irte a una carpeta donde quieras clonar el proyecto, a continuación coloca el siguiente comando `git clone https://github.com/LLuisGL/sales-insight.git`, luego abre el proyecto en tu IDE, recomendable usar **Visual Studio Code**. Una vez abierto el proyecto deberás instalar todas las dependencias, para ello coloca el comando `npm install` y esto descargará automáticamente todas las librerías usadas en el proyecto.

Para poder ejecutar el proyecto simplemente coloca `npm run dev` en la consola que te da el IDE y listo, esto abrirá una conexion al `http://localhost:5173/` y con esto tendrás parte del proyecto levantado.

El backend se levanta de manera similar, dirigete a la carpeta de backend y abrelo con tu IDE de preferencia, una vez dentro deberas de colocar en la consola `pip install -r requirements.txt`  para que instales todas las dependencias dentro, una vez hecho esto solo tendrás que colocar el siguinete comando `python manage.py runserver`, con esto ya habrás levantado el backend al cuál deberías de poder ingresar con `http://localhost:8000/`

> Nota: Dependiendo de tu máquina, puede que en el comando en vez de usar "python" debas usar "python3" o "py".

Con esto ya tienes el proyecto instalado y levantado para usar y probar todo lo que trae, eso si, teniendo la base de datos usadas.

## Rutas Hacía los Endpoints

/data <br>
║ <br>
╠→ /clients  - Extraer los top 10 clientes <br>
╠→/products - Extraer los top 20 productos <br>
╠→ /charts - Extraer información de los gráficos <br> 
╠→ /filters - Extraer información de los filtros existentes <br>
╠→ /sales - Información relevante sobre el total de ventas y venta segmentadas <br>
╠→ /count - Trae información sobre las categorias y la cantidad de compras <br>

## Notas a Tener en Cuenta

A la hora de considerar la tabla de los mejores productos usaba un id del producto, el cual debería de ser lo que lo identifica pero encontré que existían 2 productos con el mismo ID pero diferente nombre, es por eso que opté por unicamente tomar en cuenta uno de los dos IDs para la tabla.

En caso de quererse modificar bastaría con cambiar un poco la sentencia SQL pero no debería haber mayor incoveniente.

## Feedback Personal del Proyecto

Considero que esté proyecto fue interesante ya que me ayudó a comprender y establecer mejores mis conceptos sobre el lado Frontend y Backend, así mismo aprendí a usar DJango el cuál no tenía experiencia previa (He desarrollado APIs con FastAPI y Flask, con lo cuál tenía los conceptos básicos más no la sintaxis del mismo el cual tuve que ir revisando poco a poco).

Este proyecto fue hecho para una prueba técnica en un plazo máximo de 3 días, por lo cual no cuenta con todas los detalles que quisiera haberle colocado, como siguientes pasos que haría para mejorar este proyecto estaría la posibilidad de mejorar el UI/UX de la web, también organizar un poco más el código haciendo sus funciones de manera separa y no un poco monolítica como se encuentra en el proyecto y también crearía relaciones en la BD para funciones adicionales.

## Video Demo

[Aquí](https://youtu.be/tspY80FW8rU) encontrarás el video demo para desmotrar las funciones básicas de la aplicación WEB cumpliendo con los requerimientos previamente mencionados.

## Imagenes de la Aplicación WEB
![](https://i.imgur.com/Y4aNWNm.png)
![](https://i.imgur.com/vnk5YvQ.png)
![](https://i.imgur.com/pfrNLYC.png)