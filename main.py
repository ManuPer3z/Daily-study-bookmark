import json
import datetime
import calendar

LOG_FILE = "data/log.json"

def load_log():
    try:
        with open(LOG_FILE, 'r') as f:
            data = json.load(f)
            # Ensure the structure of the loaded data is correct
            if "subjects" not in data:
                data["subjects"] = []
            if "calendar" not in data:
                data["calendar"] = {}
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return {"subjects": [], "calendar": {}}

def save_log(data):
    with open(LOG_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def add_subject(subject):
    log = load_log()
    if subject not in log["subjects"]:
        log["subjects"].append(subject)
        save_log(log)

def start_study(subject):
    log = load_log()
    today = datetime.date.today().strftime("%Y-%m-%d")
    start_time = datetime.datetime.now().strftime("%H:%M:%S")
    
    if today not in log["calendar"]:
        log["calendar"][today] = {}
    
    log["calendar"][today][subject] = {
        "start_time": start_time,
        "end_time": ""
    }
        
    save_log(log)

def end_study(subject):
    log = load_log()
    today = datetime.date.today().strftime("%Y-%m-%d")
    end_time = datetime.datetime.now().strftime("%H:%M:%S")
    
    if today in log["calendar"] and subject in log["calendar"][today]:
        log["calendar"][today][subject]["end_time"] = end_time
        
    save_log(log)
    
def view_calendar():
    log = load_log()
    today = datetime.date.today()
    month_days = calendar.monthrange(today.year, today.month)[1]
    day_names = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
    # Header
    print(" " * 3 + " ".join(day_names))
    
    # Padding for the first day of the month
    first_weekday, _ = calendar.monthrange(today.year, today.month)
    print(" " * 3 * first_weekday, end="")
    
    for day in range(1, month_days + 1):
        date_str = f"{today.year}-{today.month:02d}-{day:02d}"
        if date_str in log["calendar"]:
            print(f"[{day:02d}]", end=" ")
        else:
            print(f" {day:02d} ", end=" ")
        if (day + first_weekday) % 7 == 0:  # Every Sunday, go to a new line
            print()
    print()
    
def add_topic_to_subject(subject):
    log = load_log()
    if subject not in log["subjects"]:
        log["subjects"][subject] = []

    topic = input(f"Enter the topic name for {subject}: ")
    if topic not in log["subjects"][subject]:
        log["subjects"][subject].append(topic)
        save_log(log)
        print(f"{topic} added to {subject} successfully!")
    else:
        print(f"{topic} is already in {subject}.")

def start_study_for_topic(subject):
    log = load_log()
    if subject not in log["subjects"]:
        print(f"No topics found for {subject}. Add some first.")
        return

    print(f"Topics for {subject}: {', '.join(log['subjects'][subject])}")
    topic = input("Which topic are you starting to study? ")
    
    if topic not in log["subjects"][subject]:
        print(f"{topic} not found in {subject}.")
        return
    
    today = datetime.date.today().strftime("%Y-%m-%d")
    start_time = datetime.datetime.now().strftime("%H:%M:%S")

    if today not in log["calendar"]:
        log["calendar"][today] = {}

    log["calendar"][today][topic] = {
        "start_time": start_time,
        "end_time": ""
    }

    save_log(log)



if __name__ == "__main__":
    while True:
        print("\nMenu:")
        print("1. Add a new subject")
        print("2. Start study session for a subject")
        print("3. End study session for a subject")
        print("4. View study calendar for this month")
        print("5. Exit")
        print("6. Add a topic to a subject")
        print("7. Start study session for a topic")


        choice = input("Choose an option: ")

        if choice == "1":
            subject = input("Enter the subject name: ")
            add_subject(subject)
            print(f"{subject} added successfully!")
        elif choice == "2":
            subject = input("Which subject are you starting to study? ")
            start_study(subject)
            print(f"Started studying {subject}!")
        elif choice == "3":
            subject = input("Which subject are you ending to study? ")
            end_study(subject)
            print(f"Ended studying {subject}!")
        elif choice == "4":
            view_calendar()
        elif choice == "5":
            break
        elif choice == "6":
            subject = input("Enter the subject name: ")
            add_topic_to_subject(subject)
        elif choice == "7":
            subject = input("For which subject are you starting to study? ")
            start_study_for_topic(subject)
