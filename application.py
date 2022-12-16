from flask import Flask, render_template, Response, request, redirect, url_for
import pymysql as sql
import time
import datetime

# EB looks for an 'application' callable by default.
app = Flask(__name__)

db = sql.connect(host= 'jk-db.cobd8enwsupz.us-east-1.rds.amazonaws.com',
                             user='admin',
                             password='PizAdmin',
                             port = 3306,
                             database='jk_db')

cursor = db.cursor()

@app.route("/", methods=['GET', 'POST'])
def login():    
   error = None
   if request.method == 'POST':
      if request.form['username'] != 'PizzaAdmin' or request.form['password'] != 'WeLuvPizza':
         error = 'Invalid Credentials. Please try again.'
      else:
         if db.open:
            return redirect(url_for('home'))
   return render_template('login.html', error=error) 
   
@app.route("/add_customers", methods=['GET', 'POST'])
def add_customer():
   app.logger.debug("debug log info")
   app.logger.info("Info log info")   
   error = None   
   if request.method == 'POST': 
      query = "INSERT INTO CUSTOMER(CustomerPhone, CustomerFname, CustomerLname) VALUES (%s, %s, %s)" 
      phone_num = request.form['phone_num']
      first_name = request.form['first_name']
      last_name = request.form['last_name']  
      val = (phone_num, first_name, last_name)
      cursor.execute(query, val)
      db.commit()
      return redirect('home')  
   return render_template('add_customers.html', error=error)

@app.route('/add_inventory', methods=['GET', 'POST'])
def add_inventory():
   error = None
   if request.method == 'POST':
      query = "UPDATE topping SET ToppingCurrentInventory = (ToppingCurrentInventory + %s) WHERE  toppingName = %s" 
      topping = request.form['topping']
      num= request.form['quantity']
      float(num)
      val = (num, topping)
      cursor.execute(query, val)
      db.commit()
      return redirect('home')
   return render_template('add_inventory.html', error=error) 

@app.route('/add_order', methods=['GET', 'POST'])
def add_order():
   error = None
   if request.method == 'POST':
      query = "INSERT INTO customerOrder(CustomerOrderType, CustomerOrderTimeStamp, CustomerOrderTotalCost, CustomerOrderTotalPrice, CustomerOrderIsComplete) VALUES  (%s %s %s %s %s)"
      OrderType = request.form['order_type']
      datetime_str = request.form['order_time']
      str(datetime_str)
      total_cost = request.form['order_cost']
      total_price = request.form['order_price']
      order_status = request.form['order_status']
      val = (OrderType, datetime_str, total_cost, total_price, order_status)
      cursor.execute(query, val)
      db.commit()
      phone_num = request.form['cust_num']
      query = "UPDATE customerOrder SET CustomerOrderCustomerID = CUSTOMER.CustomerID WHERE CUSTOMER.CustomerPhone = %s"
      cursor.execute(query, phone_num)
      db.commit()
      return redirect('home')
   return render_template('add_order.html', error=error)

@app.route('/progress_reports', methods=['GET', 'POST'])
def progress_reports():
   return render_template('report.html')    

@app.route('/topping_popularity', methods=['GET', 'POST'])
def topping_popularity():  
   query = "SELECT Topping, ToppingCount from ToppingPopularity order by Topping"
   cursor.execute(query)      
   data = cursor.fetchall()
   return render_template('popular_toppings.html', data=data)

@app.route('/profit_pizza', methods=['GET', 'POST'])
def profit_pizza():
   query = "SELECT * from ProfitByPizza;"  
   cursor.execute(query)
   data = cursor.fetchall()
   return render_template('pizza_profit.html', data=data)

@app.route('//profit_order', methods=['GET', 'POST'])
def profit_order():
   query = "SELECT CustomerType, OrderDate, TotalOrderPrice, TotalOrderCost, Profit from ProfitByOrderType" 
   cursor.execute(query)
   data = cursor.fetchall()
   return render_template('profit_order.html', data=data)
  

@app.route("/home", methods=['GET', 'POST'])
def home(): 
   return render_template('home.html')  

@app.route("/view_orders", methods=['GET', 'POST'])
def orders():
   query = "SELECT * FROM customerOrder"
   cursor.execute(query)
   data = cursor.fetchall()
   return render_template('orders.html', data=data)

@app.route("/view_customer", methods=['GET', 'POST'])
def customers():
   query = "SELECT * FROM CUSTOMER"  
   cursor.execute(query)
   data = cursor.fetchall()
   return render_template('customers.html', data=data)
     
@app.route("/view_inventory", methods=['GET', 'POST'])
def view_inventory():
   query = "SELECT toppingName, ToppingCurrentInventory FROM topping"
   cursor.execute(query)
   data = cursor.fetchall()
   return render_template('inventory.html', data=data)

@app.route("/logout", methods=['GET', 'POST'])  
def logout():   
   return render_template('login.html')

if __name__ == '__main__': 
   app.run(debug=True)   
