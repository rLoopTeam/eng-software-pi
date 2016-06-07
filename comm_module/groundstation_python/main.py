import htmlPy
import os
from back_end import BackEnd

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = htmlPy.AppGUI(
    title=u"Sample application")
app.static_path = os.path.join(BASE_DIR, "static/")
app.maximized = False
app.template_path = "."
app.bind(BackEnd())

app.template = ("index.html", {})

if __name__ == "__main__":
    app.start()