import sqlite3

conn = sqlite3.connect('products.db')

c = conn.cursor()
product_id = 112445
name = "testname"
product3 = "Hurkás hátú nagymamák"
url = "http://clickshop.hu/hurkashatu/nagymamak/mufogsorok"


c.execute("INSERT OR REPLACE INTO Products(id, name, keywords, url) VALUES(?,?,?,?)", (product_id, name, product3, url))
conn.commit()
conn.close()
