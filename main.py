from flask import Flask,render_template,jsonify,request,abort,url_for,redirect
from cryptography.fernet import Fernet
import hashlib
import psycopg2
import os
import paypalrestsdk
import nltk
import random
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import smtplib
import stripe
#from nltk.stem import WordNetLemmatizer
#from nltk.book import *

class AIModules:
  def __init__(self,text):
    self.text = text
  def think(self):
    #nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('all-corpora')
    nltk.download('popular')
    #tokens = word_tokenize(self.text)  # 分词
    #tokens = [token.lower() for token in tokens]  # 转换为小写
    #tokens = [token for token in tokens if token.isalpha()]  # 仅保留字母字符
    #tokens = [token for token in tokens if token not in stopwords.words("english")]  # 去除停用
    response = self.text
    return response

app = Flask("WTech")

paypalrestsdk.configure({
  'mode': 'sandbox', 
  'client_id': 'ASK8RjfrdCzGvCQRDvnfa321S_5OBGMK4KDGac5PreKf6NU-0d0MUPPrYe_S-fq4tcoHN22P8Nz4xZs3',
  'client_secret': 'EB1-tdfv74XcCxkdDWjueV19ePB4Wf8uMKwdhE2robSWQF21i6nC6pm57zzVARTzJ03ah6X4ARc1GhBQ'
})

def hash_value(user):
  u = user.encode()
  sha = hashlib.sha256(u).hexdigest()
  return sha

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/chat",methods=["POST"])
def chat():
  username = request.form.get("user")
  return jsonify({"user":username})

@app.route("/api/v1/chat/<code>",methods=["GET"])
def chatCode(code : str):
  prompt = request.form.get("prompt")
  if code == "WTech1028":
    ai = AIModules(prompt)
    response = ai.think()
    return jsonify({
       "Human-prompt" : prompt,
       "gen-prompt" : response,
       "Using module" : "FunGPT modules"
    })
  elif code == "WTech192828":
    ai = AIModules(prompt)
    response = ai.think()
    return jsonify({
       "Human-prompt" : prompt,
       "gen-prompt" : response,
       "Using module" : "FunGPT modules"
    })
  else:
    return jsonify({"Invaild code" : "Message not found"})

@app.route("/wcoin/login")
def lo():
  return render_template("wcoin.html")

@app.route("/wcoin/sk/buy/info",methods=["GET"])
def sk():
  count = int(request.args.get("price"))
  try:
    checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': count*10,
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=url_for('SKdone'),
            cancel_url=url_for('buy'),
        )
  except Exception as e:
    return str(e)

  return redirect(checkout_session.url, code=303)


@app.route("/wcoin/client",methods=["POST"])
def client():
  user = request.form.get("user")
  pw = request.form.get("pw")
  if user == "wangtry" and pw == "003417":
    count = 20000
    return render_template("client.html",user=user,count=count)
  elif user == "Cw1023" and pw == "1023":
    count = 25000000
    return render_template("client.html",user=user,count=count)
  elif user == "li-chen" and pw == "Abcd1234":
    count = 200.01
    return render_template("block.html")
  else:
    return abort(405)

@app.route("/wcoin/wcm")
def wcm():
  return render_template("wcm.html")

@app.route("/wcoin/wcm/<clientID>/<MType>")
def wcmConnect(clientID : str,MType : str):
  if clientID == "Sdcygc6766" and MType == "WM107":
    return jsonify({
        "clientID" : clientID,
        "name" : MType,
        "BlockClain id" : 51,
    })
  else:
    return jsonify({"Error 404":"Client-info not found"})

@app.route("/wcoin/pay")
def wpay_coin():
  return render_template("coin.html")

@app.route("/wcoin/pay/paypal",methods=["GET"])
def paypal_coins():
  count = request.args.get("price")
  place = request.args.get("country")
  paym = paypalrestsdk.Payment({
      "intent": "sale",
      "payer": {
          "payment_method": "paypal"
      },
      "redirect_urls": {
          "return_url": url_for('paySuccess'),
          "cancel_url": url_for('lo')
      },
      "transactions": [{
          "amount": {
              "total": count,
              "currency": place
          },
          "description": "For Wcoins"
      }]
    })
  if paym.create():
    for link in paym.links:
      if link.method == "REDIRECT":
        redirect_url = link.href
        return redirect(redirect_url)
  else:
    return jsonify({
      "msg" : "Invaild payment method!"
    })

@app.route("/wcoin/pay/success")
def paySuccess():
  return render_template("paySuccess.html")

@app.route("/wcoin/api/v1/checkUser",methods=["GET"])
def mining():
  user = request.args.get("user")
  if user == "wangtry":
    user_hash = hash_value(user=user)
    return jsonify({
       "user" : user,
       "user-api-key" : user_hash,
       "balance-on-decimal" : 200000000
    })
  elif user == "Cw1023":
    user_hash = hash_value(user=user)
    return jsonify({
       "user" : user,
       "user-api-key" : user_hash,
       "balance-on-decimal" : 25000000
    })
  else:
    return jsonify({"Invaild user":"Please correctly input!"})

@app.route("/wcoin/create/account")
def create():
  return render_template("new.html")

@app.route("/wcoin/api/v1/new_client",methods=["GET"])
def cre():
    clientID = request.args.get("clientID")
    intents = request.args.get("intents")
    fname = request.form.get("fname")
    id = request.form.get("id")
    user = request.form.get("user")
    pw = request.form.get("pw")
    with open("user.txt","a+") as f:
        fo = f"""
         User full-name: {fname}, \n
         User id: {id} \n
         --------------- \n
        """
        f.write(fo)
    return render_template("tr.html")
    
@app.route("/work/login")
def worker():
  return render_template("worker.html")

@app.route("/wtech/api/v1/login",methods=["GET"])
def checkUser():
  clientID = str(request.args.get("clientID"))
  user = request.form.get("user")
  pe = request.form.get("pw")
  if clientID == "00001":
    if user == "wangtry" and pw == "003417":
      return "success"
    else:
      return abort(502)
  else:
    return jsonify({"Invaild clientID":"Client is not verified!"})

@app.route("/wcoin/buy",methods=["GET"])
def buy():
  user = request.args.get("user")
  if user == "wangtry":
    count = 200000000
    l = [user,count]
    list_string = str(l)
    fernet = Fernet("DUBWKuYEugUex8ynVKm-7ctcUmwaV0u0JpzLkoka8_Q=")
    address = fernet.encrypt(list_string.encode()).decode()
    return render_template("buy.html",address=address)
  elif user == "Cw1023":
    count = 25000000
    l = [user,count]
    list_string = str(l)
    fernet = Fernet("DUBWKuYEugUex8ynVKm-7ctcUmwaV0u0JpzLkoka8_Q=")
    address = fernet.encrypt(list_string.encode()).decode()
    return render_template("buy.html",address=address)
  else:
    return abort(502)

@app.route("/wcoin/sell")
def sellCoin():
  return render_template("sell.html")

@app.route("/wcoin/sell/real")
def real():
  rate = random.randint(489,1000)
  return render_template("real.html",rate=rate)

@app.route("/wcoin/sell/crypto")
def crypto():
  rate = random.randint(489,1000)
  return render_template("crypto.html",rate=rate)

@app.route("/crypto/transfer/done")
def cryptoDone():
  return jsonify({"Done":"Successfully transfer! Please wait!"})

@app.route("/wcoin/transfer/cash",methods=["GET"])
def cashTransfer():
  email = request.args.get("mail")
  subject = "Client request : withdraw cash"
  content = """
  Dear Client,
     Hey, It is auto-mail,it will have staff to help you.

  Best wishes,
  W Tech Inc. technical department
  """
  s = smtplib.SMTP("smtp.gmail.com",587)
  s.starttls()
  s.login("1245server@gmail.com","jvbswpfesugcqazw")
  send_data = f"Subject: {subject} \n\n {content}"
  s.sendmail("1245server@gmail.com",email,send_data)
  return render_template("serverMail.html")

@app.route("/wcoins/mining/info")
def chAdd():
  rate = random.randint(489,1000)
  return render_template("mining.html",rate=rate)

@app.route("/wcoin/transfer/crypto",methods=["GET"])
def transferCrypto():
  address = request.form.get("address")
  amout = request.form.get("amout")
  if True:
    return render_template("cryptoTran.html",address=address,amout=amout)
  else:
    return jsonify({"Error 405":"Invaild infomation"})

@app.route("/style/css/simple")
def style():
  return render_template("style.css")

app.run(host="0.0.0.0",port=5000)
