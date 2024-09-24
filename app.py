from flask import Flask, render_template, redirect, request
from flask_mail import Mail, Message
import os

app = Flask(__name__,template_folder='./templates', static_folder='./static')

app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_USERNAME'] = 'contact@heagenbell.org'
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail()
mail.init_app(app)

def sendContactForm(result):
    msg = Message(
                  subject="Contact Form from Portfolio Website",
                  sender="contact@heagenbell.org",
                  recipients=["bellheagen@gmail.com"])
    
    msg.body = """
    
    Contact form received from Portfolio Website.
    
    Name: {}
    Email: {}
    Message: {}
    
    --End of Message--
    """.format(result['name'], result['email'], result['message'])
    
    mail.send(msg)
    
#Flask Setup
@app.route("/")
def main():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def contact():
    if request.method == "POST":
        result = {}
        
        result['name'] = request.form["name"]
        result['email'] = request.form["email"].replace(" ", "").lower()
        result['message'] = request.form["message"]

        sendContactForm(result)
        
        return render_template("index.html")
    
    return render_template("index.html")

@app.errorhandler(500)
def internal_server_error(error):
    return render_template("internal_server_error.html"), 500

if __name__ == '__main__':
    app.run(debug=True)