import sqlite3
import datetime

DB_NAME = "kinisa2.db"

conn = sqlite3.connect(DB_NAME)
conn.execute("PRAGMA foreign_keys = ON;")



def init_db():
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS students(ID INTEGER PRIMARY KEY AUTOINCREMENT,
									        FULL_NAME TAXT UNIQUE, 
									        PHONE_NUM VARCHAR(10), 
									        TOTAL_ABSCENCES INTEGER);    
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS attendance(ID INTEGER PRIMARY KEY AUTOINCREMENT,
										        STUDENT_ID INTEGER NOT NULL,
										        STATUS TEXT NOT NULL,
										        TIMESTAMP TEXT NOT NULL,
										        FOREIGN KEY (STUDENT_ID) REFERENCES students (ID));
        """
    )

    conn.commit()



def add_student():
    name = input("\nΓράψε το ονο/πωνυμο του μαθητή: ").strip()
    if not name:
        print("Το ονο/πωνυμο δεν μπορεί να είναι κενό.")
        return

    phone = input("Γράψε τον αριθμό του μαθητή: ").strip()
    if not phone:
        print("Ο αριθμός τηλεφώνου δεν μπορεί να είναι κενό.")
        return

    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (FULL_NAME, PHONE_NUM, TOTAL_ABSCENCES) VALUES(?, ?, 0)", (name, phone))

    conn.commit()

    print(f"Ο μαθητής με όνομα '{name}' προστέθηκε στο σύστημα με επιτυχία.")



def show_students():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")

    rows = cursor.fetchall()

    print("\nΠίνακας Στοιχείων όλων των Μαθητών")
    if not rows:
        print("Δεν έχουν εισαχθεί μαθητές στο Σύστημα.")
        return

    print(f"{'ID':<5} | {'Ονομ/πωνυμο':<25} | {'Τηλ/φωνο':<10} | {'Συνολικές Απουσίες':<12}")
    print("-" * 67) #Γιατί 67 😭
    for id, name, phone , total_absences in rows:
        print(f"{id:<5} | {name:<25} | {phone:<10} | {total_absences:<12}")
    


def take_attendance():
    cursor = conn.cursor()

    cursor.execute("SELECT ID, FULL_NAME, TOTAL_ABSCENCES FROM students")
    students = cursor.fetchall()

    if not students:
        print("\nΔεν υπάρχουν μαθητές στο Σύστημα.")
        return

    current_timstamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    print("Γράψε (α) για απόν και (π) για παρόν\n")

    absent_count = 0

    for id, name, total_absences in students:
        while True:
            choice = (input(f"Είναι ο/η {name} παρόν/ουσα? (α/π): ").strip().lower())
            if choice in ["α", "π", ""]:
                break
            print("Η απάντηση που δώσατε δεν ήταν μέσα στις επιλογές. Παρακαλώ πατήστε (α) για απόν, (π) για παρών ή αγήστε κενό για παρόν.")

        status = "Απόν/ούσα" if choice == "α" else "Παρόν/ούσα"

        cursor.execute("""INSERT INTO attendance(STUDENT_ID, STATUS, TIMESTAMP) VALUES(?, ?, ?)""", (id, status, current_timstamp), )
        conn.commit()

        if status == "Απόν/ούσα":
            cursor.execute("""UPDATE students SET TOTAL_ABSCENCES = TOTAL_ABSCENCES + 1 WHERE ID = ?""", (id,),)
            conn.commit()
            absent_count = absent_count + 1

    print(f"\nΠείραμε Απουσίεςςςς!!!! Σήμερα έλειπαν {absent_count} Παιδί/διά\n")



def show_attendance_logs():
    cursor = conn.cursor()

    cursor.execute(
                    """
                    SELECT logs.TIMESTAMP, students.FULL_NAME, students.PHONE_NUM, logs.STATUS
                    FROM attendance logs
                    JOIN students ON logs.STUDENT_ID = students.ID
                    ORDER BY logs.TIMESTAMP DESC
                    """
                   )
    
    rows = cursor.fetchall()

    print("\nΙστορικό Απουσιών")
    if not rows:
        print("Δεν υπάρχουν ακόμα απουσίες!")
        return

    print(f"{'Στιγμή':<20} | {'Ονομ/πωνυμο':<25} | {'Τηλ/φωνο':<10} | {'Κατάσταση':<11}")
    print("-" * 74)
    for timestamp, name, phone, status in rows:
        print(f"{timestamp:<20} | {name:<25} | {phone:<10} | {status:<11}")



def main():
    init_db()

    print("\n====================")
    print("  Σύστημα Απουσιών  ")
    print("====================")
    print("1. Πρόσθεσε Μαθητή")
    print("2. Προβολή όλων των Μαθητών")
    print("3. Πάρε Απουσίες")
    print("4. Προβολεί Ιστορικού Απουσιών")
    print("5. Έξοδος")

    while True:

        choice = input("\nΔειαλέξτε μια λειτουργεία (1-5): ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            show_students()
        elif choice == "3":
            take_attendance()
        elif choice == "4":
            show_attendance_logs()
        elif choice == "5":
            print("\nΤέλος Προγράμματος")
            break
        else:
            print("Λάθος επιλογή. Παρακαλώ επιλέξτε από τις ποιό πάνω λειτουργείες (1-5).")




if __name__ == "__main__":
    main()