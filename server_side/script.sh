# MacOS & Linux
docker build -t my_fastapi_app .
docker run -d -v /Users/alicee/Desktop/Work_Main/docker_test/server_side:/app/data -p 8000:8000 my_fastapi_app

# Windows PowerShell
#docker build -t my_fastapi_app .
#docker run -d -v C:\Users\alicee\Desktop\Work_Main\docker_test\server_side:/app/data -p 8000:8000 my_fastapi_app
