import sqlite3
import os
import atexit

def close_db(conn):
    conn.commit()
    conn.close()


def loop():
    counter=0
    conn = sqlite3.connect("classes.db")
    c = conn.cursor()
    c.execute("""
    SELECT * FROM courses;
    """)
    courses = c.fetchall()
    c.execute("""
    SELECT * FROM classrooms;
    """)
    classrooms = c.fetchall()
    numOfCourses = len(courses)
    while numOfCourses>0 and os.path.isfile('classes.db'):
        for row in classrooms:
            if row[3]==1:
                c.execute("""
                SELECT course_name FROM courses WHERE id=row[2];
                """)
                print('(' + counter + ') ' + row[1] + ': ' + c.fetchone() + " is done")
                conn.execute("""
                DELETE FROM courses WHERE id=row[2];
                """)
                numOfCourses = numOfCourses-1
                row[3]=0
            if row[3] == 0:
                c.execute("""
                SELECT * FROM courses
                WHERE class_id=row[0];
                """)
                toStart = c.fetchone()
                if not len(toStart)==0:
                    conn.executescript("""
                    UPDATE students
                    SET number_of_students = number_of_students-toStart[3]
                    WHERE students=toStart[2];
                    
                    UPDATE classrooms 
                    SET current_course_id = toStart[0] current_course_time_left=toStart[5]
                    WHERE id=row[0];
                    """)
                    print('('+counter+') '+row[1]+': '+toStart[1]+" is scheduled to start")
            else:
                c.execute("""
                SELECT course_name FROM courses WHERE id=row[2];
                """)
                print('(' + counter + ') ' + row[1] + ": occupied by" + c.fetchone())
                conn.execute("""
                UPDATE courses
                SET course_length = course_length-1
                WHERE id=row[2];
                """)
        counter = counter+1
    close_db(conn)

