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
                SELECT course_name FROM courses WHERE id=?;
                """, [row[2]])
                arr = c.fetchone()
                print('(' + str(counter) + ') ' + row[1] + ': ' + arr[0] + " is done")
                conn.execute("""
                DELETE FROM courses WHERE id=?;
                """, [row[2]])
                conn.execute("""
                UPDATE classrooms
                SET current_course_time_left=0
                WHERE current_course_id=?
                """, [row[2]])
                numOfCourses = numOfCourses-1
                row = [row[0],row[1],row[2],0]
            if row[3] == 0:
                c.execute("""
                SELECT * FROM courses
                WHERE class_id=?;
                """,[row[0]])
                toStart = c.fetchone()
                if not toStart is None:
                    conn.execute("""
                    UPDATE students
                    SET count = count - ?
                    WHERE grade=?;
                    """,[toStart[3],toStart[2]])

                    conn.execute("""
                    UPDATE classrooms 
                    SET current_course_id = ?, current_course_time_left=?
                    WHERE id=?;
                    """,[toStart[0],toStart[5] ,row[0]])
                    print('('+str(counter)+') '+row[1]+': '+toStart[1]+" is scheduled to start")
            else:
                c.execute("""
                SELECT course_name FROM courses WHERE id=?;
                """,[row[2]])
                print('(' + str(counter) + ') ' + row[1] + ": occupied by " + c.fetchone()[0])
                conn.execute("""
                UPDATE courses
                SET course_length = course_length-?
                WHERE id=?;
                """,[1,row[2]])
                conn.execute("""
                UPDATE classrooms
                SET current_course_time_left = current_course_time_left-?
                WHERE current_course_id=?;
                """, [1, row[2]])
            conn.commit()
        c.execute("""
        SELECT * FROM classrooms;
        """)
        classrooms = c.fetchall()
        counter = counter+1
    close_db(conn)

