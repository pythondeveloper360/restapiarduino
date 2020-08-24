from flask import Flask, request, render_template, redirect, session, abort, jsonify, make_response
import sql
app = Flask(__name__)
app.secret_key = "hazala"


@app.route('/', methods=["GET", "POST"])
def main():
   if request.method == "POST":
        uname = request.form.get('uname')
        password = request.form.get('pass')
        if sql.presenceOfUser(uname) == False:
            sql.signUpUser(uname, password)
            return redirect('/login')
        else:
            return render_template("signup.html", purpose='Sign Up', error='User exists')
   return render_template('signup.html', purpose='Sign Up')


@app.route('/login',methods = ["GET","POST"])
def login():
   if 'login' not in session:
      if request.method == "POST":
         uname = request.form.get('uname')
         password = request.form.get('pass')
         if sql.authenticateUser(uname, password):
            session['login'] = uname
            return sql.getApiKey(uname)[0]
   else:
      return sql.getApiKey(session["login"])[0]

   return render_template('signup.html', purpose='Login')


@app.route('/logout')
def logout():
   session.clear()
   return redirect('/login')


@app.route("/get/<apikey>/<id>")
def get_value(apikey, id):
   if request.authorization:
      userandpass = sql.getUsernameAndPasswordFromApiKey(apikey)
      if userandpass:
         if request.authorization.username == userandpass[0] and request.authorization.password == userandpass[1]:
            data = sql.getApiKey(request.authorization.username)
            if data:
               value = sql.get_value(apikey,id)
               return make_response(value, 200) if value else make_response(f"Id with {id} not found",404)
            else:
               return make_response("Not Found", 404)
         else:
               return make_response("Wrong username or password", 401)
      else:
         return "Api key is not right"
   else:
      return make_response("bad request", 400)

@app.route("/alter/<apikey>/<id>",methods = ["POST"])
def alter(apikey,id):
   if request.authorization:
      userandpass = sql.getUsernameAndPasswordFromApiKey(apikey)
      if userandpass:
         if request.authorization.username == userandpass[0] and request.authorization.password == userandpass[1]:
            rdata = request.get_json()
            data = rdata if rdata else {}
            if "value" in data:
               task = sql.alterValue(apikey,id,data)
               if task:
                  return make_response("Done",200)
               else:
                  return make_response("Wrong Apikey or ID")
            else:
               return make_response("value not given",400)
         else:
            return make_response("Wrong username or password",401)
      else:
         return make_response("bad request",400)
   else:
         return make_response("bad request",400)
      
      





if __name__ == "__main__":
    app.run(debug=True)
