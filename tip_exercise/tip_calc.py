import tornado.ioloop
import tornado.web
import tornado.log


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
  def get(self):
    self.set_header(
      'Cache-Control',
      'no-store, no-cache, must-revalidate, max-age=0')
    service_type = {"bad":0.1, "fair":0.15, "good":0.2}
    bill = self.get_query_argument('bill', '0')
    bill = float(bill)
    service = self.get_query_argument('service', 'good')
    tip_type = service_type.get(service)
    total_tip = tip_type * bill
    self.render_template('tip.html', {})

def make_app():
  return tornado.web.Application([
    (r"/", MainHandler),
  ], autoreload=True)

if __name__ == "__main__":
    tornado.log.enable_pretty_logging()
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()