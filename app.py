from flask import url_for,render_template,redirect,Flask,flash,request,session

app=Flask(__name__,static_url_path='/public')
app.config['SECRET_KEY']='bkjbeefklUDGFBLIUKB'

numbers=[['State/UT','Confirmed','Active','Recovered','Deceased'],['Arunachal Pradesh',13000,8145,2000,2000]]
total={'Confirmed':[50000,230],'Active':[30000,150],'Recovered':[18000,2300],'Deceased':[2000,10]}
colors=[['color:rgb(255, 123, 0)','background-color:rgba(255, 123, 0,0.2)'],['color:rgb(255, 0, 0)','background-color:rgba(255, 0, 0,0.2)'],
['color:rgb(0,255, 0)','background-color:rgba(0,255, 0,0.2)'],['color:rgb(77, 75, 75)','background-color:rgba(77, 75, 75,0.2)']]

@app.route('/')
def home():
    return render_template('index.html',numbers=numbers,total=list(total.items()),colors=colors)

@app.route('/SIRD')
def sird():
    return render_template('sird.html',title='SIRD Model')

@app.route('/stats')
def stats():
    return 'stats'

if __name__=="__main__":
    app.run(debug=True)