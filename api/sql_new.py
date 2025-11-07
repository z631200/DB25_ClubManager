import os
from typing import Optional
import psycopg2
from psycopg2 import pool
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
USER = os.getenv('DB_USER')
PASSWORD = os.getenv('DB_PASSWORD')
DBNAME = os.getenv('DB_NAME')
HOST = os.getenv('DB_HOST')
PORT = os.getenv('DB_PORT')

class DB:
    connection_pool = pool.SimpleConnectionPool(
        1, 100,  # 最小和最大連線數
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        dbname=DBNAME
    )

    @staticmethod
    def connect():
        return DB.connection_pool.getconn()

    @staticmethod
    def release(connection):
        DB.connection_pool.putconn(connection)

    @staticmethod
    def execute_input(sql, input):
        if not isinstance(input, (tuple, list)):
            raise TypeError(f"Input should be a tuple or list, got: {type(input).__name__}")
        connection = DB.connect()
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, input)
                connection.commit()
        except psycopg2.Error as e:
            print(f"Error executing SQL: {e}")
            connection.rollback()
            raise e
        finally:
            DB.release(connection)

    @staticmethod
    def execute(sql):
        connection = DB.connect()
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql)
        except psycopg2.Error as e:
            print(f"Error executing SQL: {e}")
            connection.rollback()
            raise e
        finally:
            DB.release(connection)

    @staticmethod
    def fetchall(sql, input=None):
        connection = DB.connect()
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, input)
                return cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error fetching data: {e}")
            raise e
        finally:
            DB.release(connection)

    @staticmethod
    def fetchone(sql, input=None):
        connection = DB.connect()
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, input)
                return cursor.fetchone()
        except psycopg2.Error as e:
            print(f"Error fetching data: {e}")
            raise e
        finally:
            DB.release(connection)


class Student:
    @staticmethod
    def get_all_student():
        sql = 'SELECT * FROM student'
        return DB.fetchall(sql, ('student',))
    
    def get_student(uid):
        sql = ''
        return DB.fetchall(sql)
    
    def create_student(input_data):
        sql = ''
        DB.execute_input(sql, (
            input_data['field1'],
            input_data['field2'],
            input_data['field3']
        ))
    
    def delete_student(uid):
        sql = ''
        DB.execute_input(sql, (uid,))

    def edit_student(input_data):
        sql = ''
        DB.execute_input(sql, (
            input_data['field1'],
            input_data['field2'],
            input_data['uid']
        ))


class Logistic:
    @staticmethod
    def get_all_logistic():
        sql = 'SELECT * FROM logistic'
        return DB.fetchall(sql)
    
    def get_logistic(lName):
        sql = ''
        return DB.fetchall(sql)
    
    def create_logistic(input_data):
        sql = ''
        DB.execute_input(sql, (
            input_data['field1'],
            input_data['field2'],
            input_data['field3']
        ))
    
    def delete_logistic(lid):
        sql = ''
        DB.execute_input(sql, (lid,))

    def edit_logistic(input_data):
        sql = ''
        DB.execute_input(sql, (
            input_data['field1'],
            input_data['field2'],
            input_data['lid']
        ))


class Equipment:
    @staticmethod
    def get_all_equipment():
        sql = 'SELECT * FROM equipment'
        return DB.fetchall(sql)
    
    def get_equipment(eid):
        sql = ''
        return DB.fetchall(sql)
    
    def create_equipment(input_data):
        sql = ''
        DB.execute_input(sql, (
            input_data['field1'],
            input_data['field2'],
            input_data['field3']
        ))
    
    def delete_equipment(eid):
        sql = ''
        DB.execute_input(sql, (eid,))

    def edit_equipment(input_data):
        sql = ''
        DB.execute_input(sql, (
            input_data['field1'],
            input_data['field2'],
            input_data['eid']
        ))


class Activity:
    @staticmethod
    def get_all_activity():
        sql = 'SELECT * FROM activity'
        return DB.fetchall(sql)
    
    def get_activity(aid):
        sql = ''
        return DB.fetchall(sql)
    
    def create_activity(input_data):
        sql = ''
        DB.execute_input(sql, (
            input_data['field1'],
            input_data['field2'],
            input_data['field3']
        ))
    
    def delete_activity(aid):
        sql = ''
        DB.execute_input(sql, (aid,))

    def edit_activity(input_data):
        sql = ''
        DB.execute_input(sql, (
            input_data['field1'],
            input_data['field2'],
            input_data['aid']
        ))


class Program:
    @staticmethod
    def get_all_program():
        sql = ''
        return DB.fetchall(sql)
    
    def get_activity_program(aSeq):
        sql = 'SELECT * FROM program WHERE aSeq = %s'
        return DB.fetchall(sql, (aSeq,))
    
    def get_program(pid):
        sql = ''
        return DB.fetchall(sql)
    
    def create_program(input_data):
        sql = ''
        DB.execute_input(sql, (
            input_data['field1'],
            input_data['field2'],
            input_data['field3']
        ))
    
    def delete_program(pid):
        sql = ''
        DB.execute_input(sql, (pid,))

    def edit_program(input_data):
        sql = ''
        DB.execute_input(sql, (
            input_data['aSeq'],
            input_data['program_id'],
            input_data['old_program_name'],
            input_data['old_program_time'],
        ))


class ParticipateActivity:
    @staticmethod
    def get_all_participate_activity():
        sql = ''
        return DB.fetchall(sql)
    
    def get_participate_activity(iaid):
        sql = ''
        return DB.fetchall(sql)
    
    def create_participate_activity(input_data):
        sql = ''
        DB.execute_input(sql, (
            input_data['field1'],
            input_data['field2'],
            input_data['field3']
        ))
    
    def delete_participate_activity(iaid):
        sql = ''
        DB.execute_input(sql, (iaid,))

    def edit_participate_activity(input_data):
        sql = ''
        DB.execute_input(sql, (
            input_data['field1'],
            input_data['field2'],
            input_data['iaid']
        ))


class PerformProgram:
    @staticmethod
    def get_all_perform_program():
        sql = ''
        return DB.fetchall(sql)
    
    def get_perform_program(ppid):
        sql = ''
        return DB.fetchall(sql)
    
    def create_perform_program(input_data):
        sql = ''
        DB.execute_input(sql, (
            input_data['field1'],
            input_data['field2'],
            input_data['field3']
        ))
    
    def delete_perform_program(ppid):
        sql = ''
        DB.execute_input(sql, (ppid,))

    def edit_perform_program(input_data):
        sql = ''
        DB.execute_input(sql, (
            input_data['field1'],
            input_data['field2'],
            input_data['ppid']
        ))


class UserEquipment:
    @staticmethod
    def get_all_user_equipment():
        sql = ''
        return DB.fetchall(sql)
    
    def get_user_equipment(ueid):
        sql = ''
        return DB.fetchall(sql)
    
    def create_user_equipment(input_data):
        sql = ''
        DB.execute_input(sql, (
            input_data['field1'],
            input_data['field2'],
            input_data['field3']
        ))
    
    def delete_user_equipment(ueid):
        sql = ''
        DB.execute_input(sql, (ueid,))

    def edit_user_equipment(input_data):
        sql = ''
        DB.execute_input(sql, (
            input_data['field1'],
            input_data['field2'],
            input_data['ueid']
        ))



# avoid error in login problem, should be merged later
class Member:
    @staticmethod
    def get_member(account):
        sql = "SELECT account, password, mid, identity, (lname || fname) AS name FROM member WHERE account = %s"
        return DB.fetchall(sql, (account,))

    @staticmethod
    def get_all_account():
        sql = "SELECT account FROM member"
        return DB.fetchall(sql)

    @staticmethod
    def create_member(input_data):
        sql = 'INSERT INTO member (lname, fname, account, password, identity) VALUES (%s, %s, %s, %s, %s)'
        DB.execute_input(sql, (
            input_data['lname'],
            input_data['fname'],
            input_data['account'],
            input_data['password'],
            input_data['identity']
        ))

    @staticmethod
    def delete_product(tno, pid):
        sql = 'DELETE FROM record WHERE tno = %s and pid = %s'
        DB.execute_input(sql, (tno, pid))

    @staticmethod
    def get_order(userid):
        sql = 'SELECT * FROM order_list WHERE mid = %s ORDER BY ordertime DESC'
        return DB.fetchall(sql, (userid,))

    @staticmethod
    def get_role(userid):
        sql = 'SELECT identity, (lname || fname) AS name FROM member WHERE mid = %s'
        return DB.fetchone(sql, (userid,))


class Analysis:
    @staticmethod
    def month_price(i):
        sql = 'SELECT EXTRACT(MONTH FROM ordertime), SUM(price) FROM order_list WHERE EXTRACT(MONTH FROM ordertime) = %s GROUP BY EXTRACT(MONTH FROM ordertime)'
        return DB.fetchall(sql, (i,))

    @staticmethod
    def month_count(i):
        sql = 'SELECT EXTRACT(MONTH FROM ordertime), COUNT(oid) FROM order_list WHERE EXTRACT(MONTH FROM ordertime) = %s GROUP BY EXTRACT(MONTH FROM ordertime)'
        return DB.fetchall(sql, (i,))

    @staticmethod
    def category_sale():
        sql = 'SELECT SUM(total), category FROM product, record WHERE product.pid = record.pid GROUP BY category'
        return DB.fetchall(sql)

    @staticmethod
    def member_sale():
        sql = '''
        SELECT SUM(price), member.mid, (member.lname || member.fname) AS name 
        FROM order_list, member 
        WHERE order_list.mid = member.mid AND member.identity = %s GROUP BY member.mid, name ORDER BY SUM(price) DESC
        '''
        return DB.fetchall(sql, ('user',))

    @staticmethod
    def member_sale_count():
        sql = '''
        SELECT COUNT(*), member.mid, (member.lname || member.fname) AS name 
        FROM order_list, member 
        WHERE order_list.mid = member.mid AND member.identity = %s GROUP BY member.mid, name ORDER BY COUNT(*) DESC
        '''
        return DB.fetchall(sql, ('user',))
