import sqlite3
import os


def close_db(conn):
    conn.commit()
    conn.close()


def print_tables(table1, table2, table3):
    print("courses")
    print(table1[0])
    print("classrooms")
    print(table2[0])
    print("students")
    print(table3[0])


def loop():
    counter = 0
    conn = sqlite3.connect("classes.db")
    c = conn.cursor()
    c.execute("""
    SELECT * FROM students;
    """)
    students = c.fetchall()
    c.execute("""
    SELECT * FROM courses;
    """)
    courses = c.fetchall()
    c.execute("""
    SELECT * FROM classrooms;
    """)
    classrooms = c.fetchall()
    num_of_courses = len(courses)
    while num_of_courses > 0 and os.path.isfile('classes.db'):
        for row in classrooms:
            if row[3] == 1:
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
                num_of_courses = num_of_courses - 1
                row = [row[0], row[1], row[2], 0]
            if row[3] == 0:
                c.execute("""
                SELECT * FROM courses
                WHERE class_id=?;
                """, [row[0]])
                to_start = c.fetchone()
                if to_start is not None:
                    conn.execute("""
                    UPDATE students
                    SET count = count - ?
                    WHERE grade=?;
                    """, [to_start[3], to_start[2]])

                    conn.execute("""
                    UPDATE classrooms 
                    SET current_course_id = ?, current_course_time_left=?
                    WHERE id=?;
                    """, [to_start[0], to_start[5], row[0]])
                    print('(' + str(counter) + ') ' + row[1] + ': ' + to_start[1] + " is scheduled to start")
            else:
                c.execute("""
                SELECT course_name FROM courses WHERE id=?;
                """, [row[2]])
                print('(' + str(counter) + ') ' + row[1] + ": occupied by " + c.fetchone()[0])
                conn.execute("""
                UPDATE courses
                SET course_length = course_length-?
                WHERE id=?;
                """, [1, row[2]])
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
        counter = counter + 1
        print_tables(courses,classrooms,students)
    close_db(conn)
