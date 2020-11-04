import psycopg2
import pandas as pd
import numpy as np
import sqlite3

dbname = 'nksgvvey'
user = 'nksgvvey'
password = 'Hr7UCoijckt9AKn1hjkW_1ZrT2_uYzVp'
host = 'lallah.db.elephantsql.com'

pg_conn = psycopg2.connect(dbname=dbname, user=user,
                            password=password, host=host)

pg_curs = pg_conn.cursor()

titanic = pd.read_csv('titanic.csv')
titanic = titanic.astype({"Survived": str, 
                            "Pclass": str})

create_titanic_table = """
CREATE TYPE sex AS ENUM ('male', 'female');
CREATE TYPE pclass AS ENUM ('1', '2', '3');
CREATE TABLE titanic (
    index SERIAL PRIMARY KEY,
    survived BOOL,
    pclass pclass,
    name VARCHAR (100),
    sex sex,
    age INT,
    siblings_spouses_aboard INT,
    parents_children_aboard INT,
    fare FLOAT
);
"""

###TABLE CREATED COMMENTED OUT BECAUSE IT THROWS AN ERROR###
pg_curs.execute(create_titanic_table)
pg_conn.commit()

for i in titanic.index:
    insert_passenger = """
        INSERT INTO titanic
        (survived, pclass, name, sex, age, siblings_spouses_aboard, parents_children_aboard, fare)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""" 
    pg_curs.execute(insert_passenger, (titanic.loc[i , "Survived"],
                                        titanic.loc[i , "Pclass"],
                                        titanic.loc[i, "Name"],
                                        titanic.loc[i , "Sex"],
                                        int(titanic.loc[i , "Age"]),
                                        int(titanic.loc[i , "Siblings/Spouses Aboard"]),
                                        int(titanic.loc[i , "Parents/Children Aboard"]),
                                        titanic.loc[i , "Fare"]) )
    

pg_conn.commit()


if __name__ == '__main__':
    #print(type(int(titanic.iloc[0][5])))
    pass