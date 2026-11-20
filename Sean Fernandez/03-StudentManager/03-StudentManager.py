
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from pathlib import Path

# File location
file_path = Path(__file__).resolve().parent / "resources" / "studentMarks.txt"

# List to store student records
students = []


# Load students from the text file
def load_students():
    global students
    students = []

    try:
        with open(file_path, "r") as file:
            lines = file.readlines()

        for line in lines[1:]:
            data = line.strip().split(",")

            if len(data) == 6:
                student = {
                    "code": data[0],
                    "name": data[1],
                    "cw1": int(data[2]),
                    "cw2": int(data[3]),
                    "cw3": int(data[4]),
                    "exam": int(data[5])
                }

                students.append(student)

    except FileNotFoundError:
        messagebox.showerror(
            "File Error",
            "studentMarks.txt could not be found!"
        )


# Save student records back to the file
def save_students():
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w") as file:
        file.write(str(len(students)) + "\n")

        for s in students:
            line = (
                s["code"] + "," +
                s["name"] + "," +
                str(s["cw1"]) + "," +
                str(s["cw2"]) + "," +
                str(s["cw3"]) + "," +
                str(s["exam"]) + "\n"
            )
            file.write(line)


# Calculate coursework total
def coursework_total(s):
    return s["cw1"] + s["cw2"] + s["cw3"]


# Calculate overall percentage
def overall_percentage(s):
    total = coursework_total(s) + s["exam"]
    return (total / 160) * 100


# Calculate student grade
def grade_for(s):
    percentage = overall_percentage(s)

    if percentage >= 70:
        return "A"
    elif percentage >= 60:
        return "B"
    elif percentage >= 50:
        return "C"
    elif percentage >= 40:
        return "D"
    else:
        return "F"


# Display text in the results area
def show_text(text):
    output.delete("1.0", tk.END)
    output.insert(tk.END, text)


# Find a student using their name or code
def find_student(search):
    for s in students:
        if s["code"].lower() == search.lower():
            return s

        if s["name"].lower() == search.lower():
            return s

    return None


# Check whether the entered marks are valid
def get_mark(title, message, maximum):
    mark = simpledialog.askinteger(
        title,
        message,
        parent=root,
        minvalue=0,
        maxvalue=maximum
    )
    return mark


# 1. View all student records
def view_all():
    if len(students) == 0:
        show_text("No student records available.")
        return

    text = "ALL STUDENT RECORDS\n"
    text += "=" * 95 + "\n"

    total_percentage = 0

    for s in students:
        percentage = overall_percentage(s)
        total_percentage += percentage

        text += (
            f"\nStudent Code: {s['code']}\n"
            f"Student Name: {s['name']}\n"
            f"Coursework Total: {coursework_total(s)}/60\n"
            f"Exam Mark: {s['exam']}/100\n"
            f"Overall Percentage: {percentage:.2f}%\n"
            f"Grade: {grade_for(s)}\n"
        )
        text += "-" * 95 + "\n"

    average = total_percentage / len(students)

    text += f"\nNumber of Students: {len(students)}"
    text += f"\nClass Average: {average:.2f}%"

    show_text(text)


# 2. View an individual student record
def view_individual():
    search = simpledialog.askstring(
        "Search Student",
        "Enter student name or student code:",
        parent=root
    )

    if not search:
        return

    s = find_student(search.strip())

    if s is None:
        messagebox.showerror("Not Found", "Student record not found.")
        return

    text = "INDIVIDUAL STUDENT RECORD\n"
    text += "=" * 45 + "\n"
    text += f"Student Code: {s['code']}\n"
    text += f"Student Name: {s['name']}\n"
    text += f"Coursework 1: {s['cw1']}/20\n"
    text += f"Coursework 2: {s['cw2']}/20\n"
    text += f"Coursework 3: {s['cw3']}/20\n"
    text += f"Coursework Total: {coursework_total(s)}/60\n"
    text += f"Exam Mark: {s['exam']}/100\n"
    text += f"Overall: {overall_percentage(s):.2f}%\n"
    text += f"Grade: {grade_for(s)}"

    show_text(text)


# 3. Show student with highest overall mark
def show_highest():
    if not students:
        show_text("No student records available.")
        return

    highest = max(students, key=overall_percentage)

    text = "HIGHEST OVERALL MARK\n"
    text += "=" * 40 + "\n"
    text += f"Name: {highest['name']}\n"
    text += f"Student Code: {highest['code']}\n"
    text += f"Percentage: {overall_percentage(highest):.2f}%\n"
    text += f"Grade: {grade_for(highest)}"

    show_text(text)


# 4. Show student with lowest overall mark
def show_lowest():
    if not students:
        show_text("No student records available.")
        return

    lowest = min(students, key=overall_percentage)

    text = "LOWEST OVERALL MARK\n"
    text += "=" * 40 + "\n"
    text += f"Name: {lowest['name']}\n"
    text += f"Student Code: {lowest['code']}\n"
    text += f"Percentage: {overall_percentage(lowest):.2f}%\n"
    text += f"Grade: {grade_for(lowest)}"

    show_text(text)


# 5. Sort student records
def sort_records():
    if not students:
        show_text("No student records available.")
        return

    choice = simpledialog.askstring(
        "Sort Records",
        "Enter A for ascending or D for descending:",
        parent=root
    )

    if choice is None:
        return

    if choice.lower() == "a":
        sorted_students = sorted(students, key=overall_percentage)
        title = "ASCENDING ORDER (LOWEST TO HIGHEST)"

    elif choice.lower() == "d":
        sorted_students = sorted(
            students,
            key=overall_percentage,
            reverse=True
        )
        title = "DESCENDING ORDER (HIGHEST TO LOWEST)"

    else:
        messagebox.showerror("Invalid Choice", "Please enter A or D.")
        return

    text = title + "\n"
    text += "=" * 55 + "\n"

    for s in sorted_students:
        text += (
            f"\n{s['name']} ({s['code']})"
            f" - {overall_percentage(s):.2f}%"
            f" - Grade {grade_for(s)}\n"
        )

    show_text(text)


# 6. Add a new student record
def add_student():
    code = simpledialog.askstring(
        "Add Student",
        "Enter student code:",
        parent=root
    )

    if not code:
        return

    code = code.strip()

    if any(s["code"] == code for s in students):
        messagebox.showerror("Error", "This student code already exists.")
        return

    name = simpledialog.askstring(
        "Add Student",
        "Enter student name:",
        parent=root
    )

    if not name or not name.strip():
        return

    name = name.strip()

    cw1 = get_mark("Coursework 1", "Enter mark out of 20:", 20)
    if cw1 is None:
        return

    cw2 = get_mark("Coursework 2", "Enter mark out of 20:", 20)
    if cw2 is None:
        return

    cw3 = get_mark("Coursework 3", "Enter mark out of 20:", 20)
    if cw3 is None:
        return

    exam = get_mark("Exam Mark", "Enter exam mark out of 100:", 100)
    if exam is None:
        return

    new_student = {
        "code": code,
        "name": name,
        "cw1": cw1,
        "cw2": cw2,
        "cw3": cw3,
        "exam": exam
    }

    students.append(new_student)
    save_students()

    messagebox.showinfo("Success", "New student has been added.")
    view_all()


# 7. Delete a student record
def delete_student():
    search = simpledialog.askstring(
        "Delete Student",
        "Enter student name or student code:",
        parent=root
    )

    if not search:
        return

    s = find_student(search.strip())

    if s is None:
        messagebox.showerror("Not Found", "Student record not found.")
        return

    answer = messagebox.askyesno(
        "Confirm Delete",
        f"Are you sure you want to delete {s['name']}?"
    )

    if answer:
        students.remove(s)
        save_students()

        messagebox.showinfo("Deleted", "Student record deleted.")
        view_all()


# 8. Update a student record
def update_student():
    search = simpledialog.askstring(
        "Update Student",
        "Enter student name or student code:",
        parent=root
    )

    if not search:
        return

    s = find_student(search.strip())

    if s is None:
        messagebox.showerror("Not Found", "Student record not found.")
        return

    choice = simpledialog.askstring(
        "Update Record",
        "What do you want to update?\n"
        "1 - Student Code\n"
        "2 - Student Name\n"
        "3 - Coursework Marks\n"
        "4 - Exam Mark",
        parent=root
    )

    if choice is None:
        return

    if choice == "1":
        new_code = simpledialog.askstring(
            "Update Code",
            "Enter new student code:",
            parent=root
        )

        if new_code and new_code.strip():
            new_code = new_code.strip()

            if any(x["code"] == new_code and x != s for x in students):
                messagebox.showerror("Error", "That code is already used.")
                return

            s["code"] = new_code

    elif choice == "2":
        new_name = simpledialog.askstring(
            "Update Name",
            "Enter new student name:",
            parent=root
        )

        if new_name and new_name.strip():
            s["name"] = new_name.strip()

    elif choice == "3":
        cw1 = get_mark("Coursework 1", "Enter new mark out of 20:", 20)
        if cw1 is None:
            return

        cw2 = get_mark("Coursework 2", "Enter new mark out of 20:", 20)
        if cw2 is None:
            return

        cw3 = get_mark("Coursework 3", "Enter new mark out of 20:", 20)
        if cw3 is None:
            return

        s["cw1"] = cw1
        s["cw2"] = cw2
        s["cw3"] = cw3

    elif choice == "4":
        exam = get_mark("Exam Mark", "Enter new exam mark out of 100:", 100)

        if exam is None:
            return

        s["exam"] = exam

    else:
        messagebox.showerror("Invalid Choice", "Please choose 1, 2, 3 or 4.")
        return

    save_students()

    messagebox.showinfo("Updated", "Student record updated successfully.")
    view_all()


# Create the main window
root = tk.Tk()
root.title("Student Manager")
root.geometry("1050x680")
root.configure(bg="#101820")
root.resizable(False, False)

# Colours
bg_colour = "#101820"
panel_colour = "#1B2A38"
button_colour = "#243B53"
text_colour = "#F1F5F9"
cyan_colour = "#35D0C5"

# Main title
title = tk.Label(
    root,
    text="STUDENT MANAGER",
    font=("Arial", 24, "bold"),
    bg=bg_colour,
    fg=cyan_colour
)
title.pack(pady=(20, 5))

subtitle = tk.Label(
    root,
    text="STUDENT RECORD MANAGEMENT SYSTEM",
    font=("Arial", 10),
    bg=bg_colour,
    fg="#AAB8C2"
)
subtitle.pack(pady=(0, 20))

# Main frame
main_frame = tk.Frame(root, bg=bg_colour)
main_frame.pack(fill="both", expand=True, padx=25, pady=10)

# Menu frame
menu_frame = tk.Frame(main_frame, bg=panel_colour, padx=15, pady=15)
menu_frame.pack(side="left", fill="y", padx=(0, 20))

menu_title = tk.Label(
    menu_frame,
    text="MAIN MENU",
    font=("Arial", 14, "bold"),
    bg=panel_colour,
    fg=cyan_colour
)
menu_title.pack(pady=(5, 15))

# Create menu buttons
menu_items = [
    ("1. View All Students", view_all),
    ("2. View Individual", view_individual),
    ("3. Highest Mark", show_highest),
    ("4. Lowest Mark", show_lowest),
    ("5. Sort Records", sort_records),
    ("6. Add Student", add_student),
    ("7. Delete Student", delete_student),
    ("8. Update Student", update_student)
]

for name, function in menu_items:
    button = tk.Button(
        menu_frame,
        text=name,
        command=function,
        font=("Arial", 10, "bold"),
        bg=button_colour,
        fg=text_colour,
        activebackground=cyan_colour,
        activeforeground="#101820",
        width=23,
        height=2,
        relief="flat",
        cursor="hand2"
    )
    button.pack(pady=5)


# Results frame
result_frame = tk.Frame(
    main_frame,
    bg=panel_colour,
    padx=15,
    pady=15
)
result_frame.pack(side="right", fill="both", expand=True)

result_title = tk.Label(
    result_frame,
    text="STUDENT INFORMATION",
    font=("Arial", 14, "bold"),
    bg=panel_colour,
    fg=cyan_colour
)
result_title.pack(anchor="w", pady=(0, 10))

# Text area for displaying results
output = tk.Text(
    result_frame,
    font=("Consolas", 10),
    bg="#0B1118",
    fg=text_colour,
    insertbackground="white",
    relief="flat",
    wrap="word",
    padx=12,
    pady=12
)
output.pack(side="left", fill="both", expand=True)

# Scrollbar
scrollbar = ttk.Scrollbar(
    result_frame,
    command=output.yview
)
scrollbar.pack(side="right", fill="y")

output.config(yscrollcommand=scrollbar.set)

# Welcome message
show_text(
    "Welcome to Student Manager!\n\n"
    "Choose an option from the menu to get started.\n\n"
    "You can view, search, sort, add, delete and update "
    "student records."
)

# Load the student records when the program starts
load_students()

# Close the program
def close_program():
    answer = messagebox.askyesno(
        "Exit",
        "Are you sure you want to close Student Manager?"
    )

    if answer:
        root.destroy()


root.protocol("WM_DELETE_WINDOW", close_program)

# Start the application
root.mainloop()
