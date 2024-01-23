import uvicorn


if __name__ == '__main__':
    uvicorn.run(host='0.0.0.0', app='check_list.asgi:application', port=6001, reload=True)
