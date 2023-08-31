from extraction import *
import mysql.connector as mysql
from mysql.connector import Error


def create_bizCard():

    connection = None
    
    try:
        connection = mysql.connect(
                            host = 'localhost',
                            database = 'biz_card',
                            user = 'root',
                            password = '#Praveenvishnu17'
                        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            print('MySQL connected successfully!')
        
        cursor.execute('DROP TABLE IF EXISTS biz_card')

        cursor.execute('''CREATE TABLE IF NOT EXISTS biz_card(
                                            id INTEGER PRIMARY KEY AUTO_INCREMENT,
                                            card_holder TEXT,
                                            company_name TEXT,
                                            designation TEXT,
                                            mobile_number VARCHAR(25),
                                            email TEXT,
                                            website TEXT,
                                            street TEXT,
                                            district TEXT,
                                            state TEXT,
                                            pincode INT,
                                            image LONGBLOB)'''
                      )

        query = '''
                INSERT INTO biz_card (card_holder, company_name, designation, mobile_number, email, 
                                          website, street, district, state, pincode, image)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)

                '''
        card = biz_card()
        
        for _, row in card.iterrows():
            values = tuple(row)
            cursor.execute(query, values)
            connection.commit()
            
    except Error as e:
        print(f'Error occured: {str(e)}')
        
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print('MySQL connection closed.')
        
create_bizCard()