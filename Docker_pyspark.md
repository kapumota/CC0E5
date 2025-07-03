### Docker y Pyspark

#### 1. Verificar que Docker Desktop esté instalado y funcionando

Antes de comenzar, asegúrate de que Docker Desktop esté instalado y corriendo en tu Windows 11. Puedes abrir una terminal (CMD, PowerShell o Git Bash) y ejecutar:

```bash
docker --version
```

Esto te confirmará que Docker está correctamente instalado.


#### 2. Descargar y ejecutar la imagen de Docker

El comando que utilizarás es:

```bash
docker run -p 8888:8888 -p 4040:4040 -v %cd%:/home/jovyan/work --name spark-jupyter -d jupyter/pyspark-notebook
```

Desglosemos lo que hace cada parte de este comando:

- **`docker run`**: Inicia un nuevo contenedor.
  
- **`-p 8888:8888`**: Mapea el puerto **8888** del contenedor (usado por Jupyter Notebook) al puerto **8888** de tu máquina. Así, podrás acceder a Jupyter a través de `http://localhost:8888`.
  
- **`-p 4040:4040`**: Mapea el puerto **4040** del contenedor (usado por la interfaz web de Spark) al mismo puerto en tu host. Esto te permitirá monitorear la interfaz de Spark.
  
- **`-v %cd%:/home/jovyan/work`**: Monta el directorio actual (donde ejecutas el comando) en el contenedor, en la ruta `/home/jovyan/work`. Esto te permite tener acceso directo a tus archivos desde el contenedor.
  
- **`--name spark-jupyter`**: Asigna el nombre **spark-jupyter** al contenedor, lo que facilita su manejo.
  
- **`-d`**: Ejecuta el contenedor en segundo plano (modo *detached*).
  
- **`jupyter/pyspark-notebook`**: Es la imagen que contiene Jupyter Notebook con PySpark, Apache Spark, SparkML y otras librerías útiles para machine learning.

*Cuando ejecutes este comando, Docker buscará la imagen en tu máquina y, si no la encuentra, la descargará automáticamente desde Docker Hub.*


#### 3. Consultar los registros del contenedor

Una vez que el contenedor esté en ejecución, necesitarás conocer la URL de Jupyter Notebook (normalmente incluye un token de acceso). Para ello, ejecuta:

```bash
docker logs spark-jupyter
```

En la salida verás información similar a:

```
    To access the notebook, open this file in a browser:
        file:///home/jovyan/.local/share/jupyter/runtime/nbserver-6-open.html
    Or copy and paste one of these URLs:
        http://127.0.0.1:8888/?token=...
```

Copia la URL (con el token) y pégala en tu navegador para acceder al entorno de Jupyter.

#### 4. Detener y reiniciar el contenedor

Cuando termines de trabajar o necesites detener el contenedor, utiliza:

```bash
docker stop spark-jupyter
```

Este comando detendrá el contenedor sin borrarlo, permitiéndote conservar la configuración y los archivos de trabajo.

Para volver a iniciarlo, ejecuta:

```bash
docker start spark-jupyter
```

Al iniciarlo, podrás acceder nuevamente al mismo entorno sin tener que reconfigurar nada.


#### 5. Usando docker desktop

Si prefieres manejar todo desde la interfaz gráfica de Docker Desktop en Windows 11, puedes hacerlo con los siguientes pasos. Ten en cuenta que muchas personas combinan la interfaz gráfica con la línea de comandos, pero aquí te muestro un flujo más centrado en Docker Desktop:

##### 5.1. Descargar la imagen desde Docker Desktop

1. **Abre Docker Desktop** en Windows 11.
2. En la parte izquierda (o superior, dependiendo de la versión) verás secciones como **Containers / Apps** e **Images**.
3. Ve a la pestaña **Images**.
4. En la esquina superior derecha, encontrarás un cuadro de búsqueda o un botón de “Pull Image”.
5. En **“Pull Image”**, escribe:  
   ```
   jupyter/pyspark-notebook
   ```  
   y haz clic en **Pull**. Esto descargará la imagen desde Docker Hub.

##### 5.2. Crear un contenedor desde la imagen

1. Una vez que termine la descarga, en la lista de **Images** aparecerá `jupyter/pyspark-notebook`.
2. Pulsa el botón **Run** (o **Create Container**) junto a la imagen.
3. Se abrirá un cuadro de diálogo donde podrás configurar:
   - **Container Name**: por ejemplo, `spark-jupyter`.
   - **Ports**: Asocia los puertos del contenedor a los puertos del host.  
     - Agrega un mapeo `8888 -> 8888` para Jupyter Notebook.  
     - Agrega un mapeo `4040 -> 4040` para la interfaz de Spark.
   - **Volumes** (opcional pero recomendado): Para que tu trabajo se guarde en tu disco local, puedes mapear una carpeta local a `/home/jovyan/work` en el contenedor.  
     - Por ejemplo, selecciona una carpeta local (por ejemplo `C:\Users\TuUsuario\proyectos`) y asígnala al contenedor en `/home/jovyan/work`.
4. Cuando termines, haz clic en **Run** (o **Create & Run**).  

De esta forma, Docker Desktop lanzará el contenedor con la configuración deseada.

##### 5.3 Ver los logs y obtener el token

1. Ve a la sección **Containers / Apps** en Docker Desktop.  
2. Localiza el contenedor que acabas de crear, por ejemplo, con nombre `spark-jupyter`.
3. Haz clic en él para ver detalles. Verás varias pestañas, como **Logs**, **Inspect**, etc.
4. Selecciona la pestaña **Logs**. Allí encontrarás la salida que normalmente verías con `docker logs` en la terminal.
5. Busca una línea similar a:
   ```
   Or copy and paste one of these URLs:
       http://127.0.0.1:8888/?token=xxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```
6. Copia **toda** la URL con el token (desde “http://127...” hasta el final).

##### 5.4. Acceder a Jupyter Notebook en el navegador

1. Abre tu navegador (Chrome, Edge, Firefox, etc.).
2. Pega la URL copiada, que contendrá el token.  
3. Presiona **Enter**.  
4. Deberías ver la interfaz de Jupyter Notebook lista para usar.  

**Si ves la pantalla de “Password or token”**, simplemente pega la parte del token (lo que va después de `?token=`) en el campo de texto y haz clic en **Sign in**.


##### 5.5 Detener e iniciar el contenedor desde Docker Desktop

- Para **detener** el contenedor, en Docker Desktop ve a la sección **Containers / Apps**, busca tu contenedor (`spark-jupyter`), haz clic en el botón de **Stop**.  
- Para **iniciarlo** de nuevo, usa el botón **Start** en la misma pantalla cuando esté detenido.

Esto equivale a usar `docker stop` y `docker start` por línea de comandos.

#### 6. (Opcional) Configurar una contraseña fija en Jupyter

Si no quieres estar usando el token cada vez, puedes configurar una contraseña persistente. Esto implica editar el archivo de configuración de Jupyter dentro del contenedor. Para hacerlo gráficamente con Docker Desktop:

1. En la pestaña **Containers / Apps**, ubica el contenedor en ejecución y abre la consola (Shell) dentro del contenedor:
   - Dependiendo de la versión de Docker Desktop, puede haber un botón **Exec** o **Open in terminal**.
2. En la consola del contenedor, ejecuta:
   ```bash
   jupyter notebook --generate-config
   ```
   Esto creará `~/.jupyter/jupyter_notebook_config.py`.
3. Genera el hash de tu contraseña:
   ```bash
   python -c "from notebook.auth import passwd; print(passwd())"
   ```
   Copia el valor (algo como `sha1:abcdef123456...`).
4. Edita el archivo de configuración:
   ```bash
   nano ~/.jupyter/jupyter_notebook_config.py
   ```
   Agrega una línea similar a:
   ```python
   c.NotebookApp.password = 'sha1:abcdef123456...'
   ```
5. Guarda y cierra el editor.
6. Detén el contenedor (desde Docker Desktop) y luego inícialo nuevamente.  
7. Ahora, en lugar de pedirte un token, Jupyter te pedirá la contraseña que configuraste.
