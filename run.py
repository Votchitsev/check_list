import uvicorn


if __name__ == '__main__':
    uvicorn.run(host='127.0.0.1', app='check_list.asgi:application', port=8080, reload=True)
