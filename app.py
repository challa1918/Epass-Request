import requests
from flask import Flask,render_template,request
from twilio.rest import Client


account_sid = "AC33ae3a28a69bf8d6259558ef43c1d3c9"
auth_token = "2f132513aaf787386145d15cfdedb621"

client = Client(account_sid,auth_token)
app = Flask(__name__,static_url_path='/static')

@app.route("/")
def registration_form():
    return render_template('Index.html')

@app.route('/login_Page',methods = ["POST","GET"])
def login_registration_dtls():
    first_name = request.form["fname"]
    last_name = request.form["lname"]
    email_id = request.form['email']
    source_st = request.form['source_state']
    source_dt = request.form['source']
    destination_st = request.form["dest_state"]
    destination_dt = request.form['dest_district']
    phoneNumber = request.form['phone']
    id_proof = request.form['idcard']
    date = request.form['trip']
    full_name = first_name + "-" + last_name
    r = requests.get("https://api.covid19india.org/v4/data.json")
    json_data = r.json()
    cnt = json_data[destination_st]['districts'][destination_dt]['total']['confirmed']
    pop = json_data[destination_st]['districts'][destination_dt]['meta']['population']
    travel_pass = ((cnt/pop)*100)
    status = ""
    if(travel_pass < 30 and request.method == 'POST'):
        status = "CONFIRMED"
    else:
        status = "NOT CONFIRMED"

    message = client.messages.create(to = "whatsapp:+918099519595",
                           from_ = "whatsapp:+14155238886",
                            body = "Hello "+full_name+" "+"Your Travel Pass From "+" "+source_dt+" To "+" "+destination_dt+
                            " Of "+" "+destination_st+" State is "+" "+status)
    print(message)
    return render_template('user_registration_dtls.html',var = full_name,var1 = email_id,var2 = id_proof,
                            var3 = source_st,var4 = source_dt,var5 = destination_st,var6 = destination_dt,
                           var7 = phoneNumber,var8 = date,var9 = status)

if __name__ == "__main__":
    app.run(port = 9001,debug = True)






