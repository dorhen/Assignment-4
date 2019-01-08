import sqlite3
import optparse
import os



def main():
    file_exist = os.path.isfile('schedule.db')
    if not file_exist:
        conn = sqlite3.connect("schedule.db")
        conn.executescript("""
                CREATE TABLE courses (
                id INTEGER PRIMARY KEY,
                course_name TEXT NOT NULL,
                student TEXT NOT NULL,
                number_of_students INTEGER NOT NULL,
                class_id INTEGER REFERENCES  classrooms(id),
                course_length INTEGER NOT NULL
                );

                CREATE TABLE students (
                grade TEXT PRIMARY KEY,
                count INTEGER NOT NULL
                );

                CREATE TABLE classrooms (
                id INTEGER PRIMARY KEY,
                location TEXT NOT NULL,
                current_course_id INTEGER NOT NULL,
                current_course_time_left INTEGER NOT NULL 
                );
            """)
        parser = optparse.OptionParser()
        args = parser.parse_args()
        file_object = open(args[1][0], "r")
        for line in file_object:
            line = line.rstrip()
            line = line.replace(' ,',',')
            line = line.replace(', ',',')
            split = line.split(',')
            if split[0] == 'C':
                conn.execute("""
                INSERT INTO courses(id,course_name,student,number_of_students,class_id,course_length) VALUES (?,?,?,?,?,?);
                """, split[1:])
            if split[0] == 'S':
                conn.execute("""
                INSERT INTO students(grade,count) VALUES (?,?);
                """, split[1:])
            if split[0] == 'R':
                ans = split[1:] + ["0", "0"]
                conn.execute("""
                    INSERT INTO classrooms(id,location,current_course_id,current_course_time_left) VALUES (?,?,?,?);
                    """, ans)
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
        print_tables(courses, classrooms, students)
        close_db(conn)

def print_tables(table1, table2, table3):
    print("courses")
    for line in table1:
        print(line)
    print("classrooms")
    for line in table2:
        print(line)
    print("students")
    for line in table3:
        print(line)


def close_db(conn):
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()
