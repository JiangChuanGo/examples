from bottle import route, run, template, request, post

@post('/msg')
def index():
    print(request.body.read().decode("utf-8"))
    return "<h1>OK</h1>"

run(host='localhost', port=8080)
