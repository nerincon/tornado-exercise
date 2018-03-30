import tornado.ioloop
import tornado.web
import tornado.log

import os
import boto3

client = boto3.client(
  'ses',
  region_name='us-east-1',
  aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
  aws_secret_access_key=os.environ.get('AWS_SECRET_KEY')
)


def send_email(name,email, message):
    response = client.send_email(
    Destination={
        'ToAddresses': ['nerincon1@gmail.com'],
    },
    Message={
        'Body': {
        'Text': {
            'Charset': 'UTF-8',
            'Data': ('Sender Name: {}\n''Email from sender:{}\n''Message from Sender:{}'.format(name,email,message))
        },
        },
        'Subject': {'Charset': 'UTF-8', 'Data': 'Test email'},
    },
    Source='nerincon1@gmail.com',
    )


from jinja2 import \
  Environment, PackageLoader, select_autoescape

ENV = Environment(
  loader=PackageLoader('myapp', 'templates'),
  autoescape=select_autoescape(['html', 'xml'])
)

class TemplateHandler(tornado.web.RequestHandler):
  def render_template (self, tpl, context):
    template = ENV.get_template(tpl)
    self.write(template.render(**context))

class MainHandler(TemplateHandler):
  def get(self, page='index'):
    page = page + '.html'
    self.set_header(
      'Cache-Control',
      'no-store, no-cache, must-revalidate, max-age=0')
    self.render_template(page, {})

class SuccessHandler(TemplateHandler):
  def get(self):
    self.set_header(
      'Cache-Control',
      'no-store, no-cache, must-revalidate, max-age=0')
    self.render_template("contact.html", {})

  def post (self):
    name = self.get_body_argument('name', None)
    email = self.get_body_argument('email', None)
    message = self.get_body_argument('message', None)
    error = ''
    if email:
      print('Name:',name , 'EMAIL:', email)
      send_email(name, email, message)
      self.redirect('/contact-success')
      
    else:
      error = 'Please fill in your email in the email box'
    self.set_header(
      'Cache-Control',
      'no-store, no-cache, must-revalidate, max-age=0')
    self.render_template("contact.html", {'error': error})

    
def make_app():
  return tornado.web.Application([
    (r"/", MainHandler),
    (r"/(hobbies)", MainHandler),
    (r"/(portfolio)", MainHandler),
    (r"/(contact-success)", MainHandler),
    (r"/contact", SuccessHandler),
    (
      r"/static/(.*)",
      tornado.web.StaticFileHandler,
      {'path': 'static'}
    ),
  ], autoreload=True)
  
if __name__ == "__main__":
  tornado.log.enable_pretty_logging()
  
  app = make_app()
  PORT = int(os.environ.get('PORT', '8000'))
  app.listen(PORT)
  tornado.ioloop.IOLoop.current().start()