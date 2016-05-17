import htmlPy
from back_end import BackEnd

app = htmlPy.AppGUI(
    title=u"Sample application")
app.maximized = True
app.template_path = "."
app.bind(BackEnd())

app.template = ("index.html", {})

if __name__ == "__main__":
    app.start()