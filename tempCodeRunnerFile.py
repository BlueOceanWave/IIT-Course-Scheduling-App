
            #     cursor.execute(termQuery, termValues)
            # except:
            #     print(f"Couldn't add term for {course_data['sID']} {course_data['cID']}")

            # try:
            #     cursor.execute(classQuery, classValues)
            # except:
            #     print(f"Couldn't add class {course_data['sID']} {course_data['cID']}")

            # try:
            #     # Execute query for each instructor
            #     for instructor in course_data['instructors']:
            #         instructorQuery = "INSERT INTO instructors (CRN, instructor) VALUES (%s, %s)"
            #         instructorValues = (course_data['CRN'], instructor)
            #         cursor.execute(instructorQuery, instructorValues)
            # except:
            #     print(f"Couldn't add instructors f