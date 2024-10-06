<h1> Aqui iran todos lo archivos de la semana de django</h1>
<p>Para que esto funcione correctamente teneos que activar el entorno virtual y usar el sqlite3</p>
<h2>Pasos para ejecucion</h2>
<ul>
  Usar sin contar las comillas
  <li>Crear el entorno Virutal en una carpeta luego usar "python -m venv myvenv"</li>
  <li>Acceder a al entorno virtual con el comando: "myvenv\Scripts\activate"</li>
  <li>"pip install django"</li>
  <li>"cd lab03"</li>
  <li>"python manage.py makemigrations encuesta"</li>
  <li>"python manage.py sqlmigrate encuesta 0002"</li>
  <li>"python manage.py migrate"</li>
  <li>"python manage.py runserver"</li><br>
  finalmente podra ver el proyecto en el navegador.La ruta a usar muy probablemete "http://127.0.0.1:8000/encuesta/autos/"
</ul>
<warnig> Cabe destacar que para que todo lo anterior funcione tiene que tener Python, pip instalado en su computadora...</warnig>

<h2>Django_Crud_api</h2>
<p>Tiene una api creada que levanta en un puerto y los estilos tienen que poner que se levante en otro puerto</p>


<h2>Correr el lab_07</h2>
<p>cd lab07</p>
<p>python manage.py  runserver</p>
<p>http://localhost:8000</p>

