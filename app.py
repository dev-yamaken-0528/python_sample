from bottle import route, template, static_file, request, run
from datetime import datetime
from chat import chat
from meet import meet


@route('/')
def app_top():
  return template('app.html')


@route('/chat')
def chat_top():
  tmp = "is chat"
  return template('chat.html', msg=tmp)

@route('/chat', method="POST")
def chat_post():
  reply = chat.make_reply(request.forms.inputmsg)
  return reply


@route('/meet')
def meet_top():
  return template('meet.html', title="top", filename="noimage.jpg", results="")

@route('/meet', method="POST")
def meet_upload():
  upload = request.files.get('upload','')
  upload.filename = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
  upload.save("./meet/images/")
  results = meet.label_image("./meet/images/"+upload.filename)
  return template('meet.html', title="upload", filename=upload.filename, results=results)

@route('/meet/images/<filename:path>')
def public(filename):
  return static_file(filename, root="./meet/images/")


run(host="0.0.0.0",port=3000)
