from flask import Flask, render_template, json, request
from flaskext.mysql import MySQL
import memcache
import time
from random import randrange,uniform
from passlib.hash import sha256_crypt


#memcache connection
client=memcache.Client(['memcache arn'],debug=True)


mysql = MySQL()
app = Flask(__name__)

#mysql credentials
app.config['MYSQL_DATABASE_USER'] = '###'
app.config['MYSQL_DATABASE_PASSWORD'] = '###'
app.config['MYSQL_DATABASE_DB'] = '###'
app.config['MYSQL_DATABASE_HOST'] = '###'
mysql.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query')
def query():

    #taking user input
    #age = request.args.get('age')

    cache = 0
    db = 0

    start=time.time()
    #for running 5000 queries to memcache.
    #If query and result is present in memcache, then display result
    #Else, query database and update the same to memcache for future quering
    for i in range(1,5001):

        #randomized age value
        age= str(randrange(1,31))
        print age

        query='select name from boats where age='+age

        #creating the memcache key based on age
        key='age_equals_'+age

        ## Key creation by hashing using either use hash or encrypt
        # encrypt=sha256_crypt.encrypt(query)
        # print encrypted_key
        # hash_key=sha256_crypt.hash(query)
        # print hash_key



        ##Checking if data is in memcache
        data = client.get(key)
        if data:
            cache+=1

        ## Else checking in DB
        else:
            conn = mysql.connect()
            print 'mysql connected'

            cursor = conn.cursor()
            print 'cursor creted'
            print 'querying'

            cursor.execute(query)
            print 'fetching data'
            result = cursor.fetchall()

            # Updating in memcache
            client.set(key, result,60)
            print 'saved data onto cache'

            conn.commit()
            conn.close()

            db+=1

    end=time.time()
    total=end-start

    #return the count of queries done to memcache and db respectively
    return '5000 queries done!. The number of queries to cache is: {0} and number of queries to db is {1}. And the time taken is {2}'.format(cache,db,total)


if __name__ == '__main__':
    app.run(debug=True)


###############################################################3

# range - prints from 1 to 4.. with step of 1.. for 5 also to be inclusove.. give range(1,6)
#     for i in range(1,5,1):
#         print i

#randrange - generates a single random "int" number given in the range
    # age_range= randrange(1,5)
    # print age_range

#uniform - genereates random float number within the range.. eg: 4.776767777
    # age_range= uniform(1,5)
    # print age_range

