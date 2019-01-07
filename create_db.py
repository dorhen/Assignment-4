import sqlite3
import optparse
import os
import schedule

if __name__ == '__main__':
    for i in os.listdir():
        print(i)
    fileExist =os.path.isfile('classes.db')
    if not fileExist:
        conn = sqlite3.connect("classes.db")
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
        file_object = open(args[1][0])
        for line in file_object:
            split=line.split(', ')
            if split[0]=='C':
                conn.execute("""
                INSERT INTO courses(id,course_name,student,number_of_students,class_id,course_length) VALUES (?,?,?,?,?,?);
                """, split[1:])
            if split[0]=='S':
                conn.execute("""
                INSERT INTO students(grade,count) VALUES (?,?);
                """, split[1:])
            if split[0]=='R':
                ans=split[1:]+[-1,0]
                conn.execute("""
                INSERT INTO classrooms(id,location,current_course_id,current_course_time_left) VALUES (?,?,?,?);
                """, ans)
        conn.commit()
        schedule.loop()


