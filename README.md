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
