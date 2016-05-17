import htmlPy


class BackEnd(htmlPy.Object):

    @htmlPy.Slot()
    def say_hello_world(self):
        from main import app
        app.html = u"Hello, world"