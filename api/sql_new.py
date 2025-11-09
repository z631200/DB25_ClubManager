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
        return DB.fetchall(sql)
    
    @staticmethod
    def get_student(sId):
        sql = 'SELECT * FROM student WHERE sId = %s'
        return DB.fetchall(sql, (sId,))


    @staticmethod
    def create_student(input_data):
        sql = '''
            INSERT INTO Student (sId, sName, gender, Grade, Department, isMember, lName)
            VALUES (%s, %s, %s, %s, %s, %s, NULLIF(%s, ''))
        '''
        DB.execute_input(sql, (
            input_data['sId'],
            input_data['sName'],
            input_data['gender'],
            input_data['grade'],
            input_data['department'],
            input_data['isMember'],
            input_data['logistic']
        ))

    @staticmethod
    def delete_student(sId):
        sql = 'DELETE FROM Student WHERE sId = %s'
        DB.execute_input(sql, (sId,))

    @staticmethod
    def update_student(input_data):
        sql = '''
            UPDATE Student SET sName = %s, gender = %s, grade = %s,
              department = %s, isMember = %s, lName = NULLIF(%s, '') WHERE sId = %s
        '''
        DB.execute_input(sql, (
            input_data['sName'],
            input_data['gender'],
            input_data['grade'],
            input_data['department'],
            input_data['isMember'],
            input_data['logistic'],
            input_data['sId']
        ))


class Logistic:
    @staticmethod
    def get_all_logistic():
        sql = 'SELECT * FROM logistic'
        return DB.fetchall(sql)
    
    @staticmethod
    def get_logistic(lName):
        sql = 'SELECT * FROM logistic WHERE lName = %s'
        return DB.fetchall(sql, (lName,))

    @staticmethod
    def create_logistic(input_data):
        sql = '''
            INSERT INTO logistic (lName, Job_Desc) VALUES (%s, %s)
        '''
        DB.execute_input(sql, (
            input_data['lName'],
            input_data['Job_Desc'],
        ))
    
    @staticmethod
    def delete_logistic(lName):
        sql = 'DELETE FROM logistic WHERE lName = %s'
        DB.execute_input(sql, (lName,))

    @staticmethod
    def update_logistic(input_data):
        sql = '''
            UPDATE logistic SET lName = %s, Job_Desc = %s WHERE lName = %s
        '''
        DB.execute_input(sql, (
            input_data['new_lName'],
            input_data['Job_Desc'],
            input_data['lName']
        ))


class Equipment:
    @staticmethod
    def get_all_equipment():
        sql = 'SELECT * FROM Equipment'
        return DB.fetchall(sql)
    
    @staticmethod
    def get_equipment(eID):
        sql = 'SELECT * FROM Equipment WHERE eID = %s'
        return DB.fetchall(sql, (eID,))

    @staticmethod
    def create_equipment(input_data):
        sql = '''
            INSERT INTO Equipment (eID, eName, eLocation, Quantity, Note, lName)
            VALUES (%s, %s, %s, %s, %s, NULLIF(%s, ''))
        '''
        DB.execute_input(sql, (
            input_data['eId'],
            input_data['eName'],
            input_data['eLocation'],
            input_data['Quantity'],
            input_data['Note'],
            input_data['lName']
        ))
    
    @staticmethod
    def delete_equipment(eID):
        sql = 'DELETE FROM Equipment WHERE eID = %s'
        DB.execute_input(sql, (eID,))

    @staticmethod
    def update_equipment(input_data):
        sql = '''
            UPDATE Equipment SET eName = %s, eLocation = %s, Quantity = %s,
              Note = %s, lName = NULLIF(%s, '') WHERE eID = %s
        '''
        DB.execute_input(sql, (
            input_data['eName'],
            input_data['eLocation'],
            input_data['Quantity'],
            input_data['Note'],
            input_data['lName'],
            input_data['eId'],
        ))


class Activity:
    @staticmethod
    def get_all_activity():
        sql = 'SELECT * FROM activity'
        return DB.fetchall(sql)
    
    @staticmethod
    def get_activity(aSeq):
        sql = 'SELECT * FROM activity WHERE aSeq = %s'
        return DB.fetchall(sql, (aSeq,))

    @staticmethod
    def create_activity(input_data):
        sql = '''
            INSERT INTO activity (aSeq, aName, activityDate, aLocation)
            VALUES (%s, %s, %s, %s)
        '''
        DB.execute_input(sql, (
            input_data['aSeq'],
            input_data['aName'],
            input_data['activityDate'],
            input_data['aLocation']
        ))

    @staticmethod
    def delete_activity(aSeq):
        sql = 'DELETE FROM activity WHERE aSeq = %s'
        DB.execute_input(sql, (aSeq,))

    @staticmethod
    def update_activity(input_data):
        sql = '''
            UPDATE activity SET aName = %s, activityDate = %s, aLocation = %s WHERE aSeq = %s
        '''
        DB.execute_input(sql, (
            input_data['aName'],
            input_data['activityDate'],
            input_data['aLocation'],
            input_data['aSeq']
        ))


class Program:
    # @staticmethod
    # def get_all_program():
    #     sql = ''
    #     return DB.fetchall(sql)

    @staticmethod
    def get_activity_program(aSeq):
        sql = 'SELECT * FROM program WHERE aSeq = %s'
        return DB.fetchall(sql, (aSeq,))
    
    @staticmethod
    def get_program(aSeq, programTime):
        sql = 'SELECT * FROM program WHERE aSeq = %s AND programTime = %s'
        return DB.fetchall(sql, (aSeq, programTime))

    @staticmethod
    def create_program(input_data):
        print(input_data)
        sql = 'INSERT INTO program (aSeq, programTime, Song) VALUES (%s, %s, %s)'
        DB.execute_input(sql, (
            input_data['aSeq'],
            input_data['programTime'],
            input_data['Song']
        ))

    @staticmethod
    def delete_program(aSeq, programTime):
        sql = 'DELETE FROM program WHERE aSeq = %s AND programTime = %s'
        DB.execute_input(sql, (aSeq, programTime))

    @staticmethod
    def update_program(input_data):
        sql = '''
            UPDATE program SET programTime = %s, Song = %s 
            WHERE aSeq = %s AND programTime = %s
        '''
        print(f"input_data: {input_data}")
        DB.execute_input(sql, (
            input_data['new_programTime'],
            input_data['Song'],
            input_data['aSeq'],
            input_data['programTime']
        ))


class StudentJoin:
    @staticmethod
    def get_all_participate_activity():
        sql = 'SELECT * FROM StudentJoin'
        return DB.fetchall(sql)
    
    # @staticmethod
    # def get_participate_activity_by_student(sId):
    #     sql = '''
    #         SELECT sj.sID, s.sName
    #         FROM StudentJoin sj
    #         JOIN Student s ON sj.sID = s.sID
    #         WHERE sj.sID = %s
    #     '''
    #     return DB.fetchall(sql, (sId,))
    
    @staticmethod
    def get_participate_activity_by_activity(aSeq):
        sql = '''
            SELECT sj.sID, s.sName
            FROM StudentJoin sj
            JOIN Student s ON sj.sID = s.sID
            WHERE sj.aSeq = %s
        '''
        return DB.fetchall(sql, (aSeq,))
    
    @staticmethod
    def get_participate_activity(aSeq, sId):
        sql = '''
            SELECT sj.sID, s.sName
            FROM StudentJoin sj
            JOIN Student s ON sj.sID = s.sID
            WHERE sj.aSeq = %s AND sj.sID = %s
        '''
        return DB.fetchall(sql, (aSeq, sId, ))

    @staticmethod
    def create_participate_activity(input_data):
        sql = 'INSERT INTO StudentJoin (aSeq, sId) VALUES (%s, %s)'
        DB.execute_input(sql, (
            input_data['aSeq'],
            input_data['sId']
        ))
    
    @staticmethod
    def delete_participate_activity(aSeq, sId):
        sql = 'DELETE FROM StudentJoin WHERE aSeq = %s AND sId = %s'
        DB.execute_input(sql, (aSeq, sId, ))

    # def edit_participate_activity(input_data):
    #     sql = ''
    #     DB.execute_input(sql, (
    #         input_data['field1'],
    #         input_data['field2'],
    #         input_data['iaid']
    #     ))


class PerformProgram:

    @staticmethod
    def get_all_perform():
        sql = 'SELECT * FROM StudentPerform'
        return DB.fetchall(sql)
    
    # @staticmethod
    # def get_perform_by_student(sId):
    #     sql = '''
    #         SELECT p.sID, s.sName
    #         FROM StudentPerform p
    #         JOIN Student s ON p.sID = s.sID
    #         WHERE p.sID = %s
    #     '''
    #     return DB.fetchall(sql, (sId,))
    
    @staticmethod
    def get_perform_by_programTime(aSeq, programTime):
        sql = '''
            SELECT p.sID, s.sName
            FROM StudentPerform p
            JOIN Student s ON p.sID = s.sID
            WHERE p.aSeq = %s AND p.programTime = %s
        '''
        return DB.fetchall(sql, (aSeq, programTime, ))
    
    @staticmethod   
    def get_perform(sId, aSeq, programTime):
        sql = '''
            SELECT p.sID, s.sName
            FROM StudentPerform p
            JOIN Student s ON p.sID = s.sID
            WHERE p.sID = %s AND p.aSeq = %s AND p.programTime = %s
        '''
        return DB.fetchall(sql, (sId, aSeq, programTime))
    
    @staticmethod
    def create_perform(input_data):
        sql = 'INSERT INTO StudentPerform (sId, aSeq, programTime) VALUES (%s, %s, %s)'
        DB.execute_input(sql, (
            input_data['sId'],
            input_data['aSeq'],
            input_data['programTime']
        ))      

    @staticmethod
    def delete_perform(sId, aSeq, programTime):
        sql = 'DELETE FROM StudentPerform WHERE aSeq = %s AND sId = %s AND programTime = %s'
        DB.execute_input(sql, (aSeq, sId, programTime))


class UseEquipment:
    @staticmethod
    def get_all_use_equipment():
        sql = 'SELECT * FROM EquipmentUse'
        return DB.fetchall(sql)
    
    @staticmethod
    def get_use_equipment_by_program(aSeq, programTime):
        sql = '''
            SELECT e.eID, e.eName, e.eLocation, e.Quantity, e.Note, e.lName
            FROM EquipmentUse u
            JOIN Equipment e
            ON u.eID = e.eID
            WHERE u.aSeq = %s
            AND u.programTime = %s
        '''
        return DB.fetchall(sql, (aSeq, programTime, ))
    
    @staticmethod
    def get_use_equipment(eID, aSeq, programTime):
        sql = '''
            SELECT e.eID, e.eName, e.eLocation, e.Quantity, e.Note, e.lName
            FROM EquipmentUse u
            JOIN Equipment e
            ON u.eID = e.eID
            WHERE e.eID = %s
            AND u.aSeq = %s
            AND u.programTime = %s
        '''
        return DB.fetchall(sql, (eID, aSeq, programTime, ))
    
    @staticmethod
    def create_use_equipment(input_data):
        sql = 'INSERT INTO EquipmentUse (eID, aSeq, programTime) VALUES (%s, %s, %s)'
        DB.execute_input(sql, (
            input_data['eId'],
            input_data['aSeq'],
            input_data['programTime']
        ))  

    @staticmethod
    def delete_use_equipment(eID, aSeq, programTime):
        sql = 'DELETE FROM EquipmentUse WHERE eID = %s AND aSeq = %s AND programTime = %s'
        DB.execute_input(sql, (eID, aSeq, programTime))


class Analysis:
    @staticmethod
    def count_participants():
        sql = '''
            SELECT A.aName AS 活動名稱, COUNT(SJ.sID) AS 參加人數
            FROM Activity AS A
            JOIN StudentJoin AS SJ ON A.aSeq = SJ.aSeq
            GROUP BY A.aName;
        '''
        return DB.fetchall(sql)

    @staticmethod
    def activity_detail():
        sql = '''
            SELECT A.aName AS 活動名稱, P.Song AS 節目名稱, S.sName AS 表演者
            FROM Activity AS A
            JOIN Program AS P ON A.aSeq = P.aSeq
            JOIN StudentPerform AS F ON P.aSeq = F.aSeq AND P.programTime  = F.programTime
            JOIN Student AS S ON F.sID = S.sID
            ORDER BY A.aSeq, P.programTime;
        '''
        return DB.fetchall(sql)
    
    @staticmethod
    def equipment_usage():
        sql = '''
            SELECT P.Song AS 節目名稱, E.eName AS 器材名稱, E.Quantity AS 數量
            FROM Program AS P
            JOIN EquipmentUse AS U ON P.aSeq = U.aSeq AND P.programTime = U.programTime
            JOIN Equipment AS E ON U.eID = E.eID
            ORDER BY P.Song;
        '''
        return DB.fetchall(sql)
    
    @staticmethod
    def student_participation(sName): 
        sql = ''' 
            SELECT S.sID, S.sName, A.aName AS 活動名稱
            FROM Student AS S 
            JOIN StudentJoin AS SJ ON S.sID = SJ.sID 
            JOIN Activity AS A ON SJ.aSeq = A.aSeq 
            WHERE S.sName = %s; 
        ''' 
        return DB.fetchall(sql, (sName,))
    
    @staticmethod
    def equipment_belongs():
        sql = '''
            SELECT L.lName AS 組別, E.eName AS 器材名稱, S.sName AS 成員
            FROM Logistic AS L
            JOIN Equipment AS E ON L.lName = E.lName
            LEFT JOIN Student AS S ON L.lName = S.lName
            ORDER BY L.lName, E.eName;
        '''
        return DB.fetchall(sql)
