import pandas as pd
import random
import os
from datetime import datetime, timedelta

random.seed(42)

# Ensure data directory exists
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
os.makedirs(DATA_DIR, exist_ok=True)

# Sri Lankan Context Data
SL_FIRST_NAMES = ['Kamal', 'Nimal', 'Sunil', 'Kasun', 'Dasun', 'Nuwan', 'Lahiru', 'Sandun', 'Chamara', 'Saman',
                  'Amila', 'Gayan', 'Tharindu', 'Dinesh', 'Ruwan', 'Nayana', 'Sashika', 'Kavindu', 'Malith', 'Heshan',
                  'Nethmi', 'Oshadi', 'Tharushi', 'Kavindi', 'Dinithi', 'Sandali', 'Hiruni', 'Sachini', 'Upeka', 'Nimesha',
                  'Piumi', 'Hansani', 'Dilani', 'Harshani', 'Madushani', 'Sewwandi', 'Nimanthi', 'Ashani', 'Nadeesha']

SL_LAST_NAMES = ['Perera', 'Silva', 'Fernando', 'De Silva', 'Bandara', 'Kumara', 'Ratnayake', 'Dissanayake', 
                 'Weerasinghe', 'Rajapaksha', 'Jayawardena', 'Senanayake', 'Wickramasinghe', 'Liyanage', 'Gunawardena',
                 'Karunaratne', 'Jayasinghe', 'Ranasinghe', 'Samarasinghe', 'Munasinghe', 'Siriwardena', 'Balasuriya']

SL_UNIVERSITIES = ['UCSC', 'UoM (Moratuwa)', 'UoP (Peradeniya)', 'UoK (Kelaniya)', 'UoJ (Jaffna)', 'UoR (Ruhuna)', 'SJP (Japura)', 'Wayamba']

def generate_students(num_students=500):
    faculties = ['Computing', 'Engineering', 'Science', 'Management', 'Arts']
    degrees = {
        'Computing': ['BSc Computer Science', 'BSc Software Engineering', 'BSc Information Systems'],
        'Engineering': ['BSc Civil Eng', 'BSc Mechanical Eng', 'BSc Electrical Eng', 'BSc Electronic & Telecom'],
        'Science': ['BSc Physical Science', 'BSc Biological Science', 'BSc Chemistry Special'],
        'Management': ['BSc Business Administration', 'BSc Accounting', 'BSc Human Resource Mgt'],
        'Arts': ['BA English', 'BA Economics', 'BA Mass Media']
    }
    all_interests = ['Coding', 'Music', 'Cricket', 'Robotics', 'Business', 'Art', 'Debate', 'Gaming', 'AI', 'Networking', 'Photography', 'Volunteering']
    
    students = []
    for i in range(1, num_students + 1):
        faculty = random.choice(faculties)
        degree = random.choice(degrees[faculty])
        uni = random.choice(SL_UNIVERSITIES)
        interests = ", ".join(random.sample(all_interests, k=random.randint(1, 3)))
        
        # Generate a Sri Lankan Name
        name = f"{random.choice(SL_FIRST_NAMES)} {random.choice(SL_LAST_NAMES)}"
        
        students.append({
            'student_id': f"S{i:04d}",
            'name': name,
            'university': uni,
            'faculty': faculty,
            'degree': degree,
            'year': random.randint(1, 4),
            'interests': interests
        })
    return pd.DataFrame(students)

def generate_events(num_events=100):
    categories = ['Hackathon', 'Musical Show', 'Sports Meet', 'Tech Talk', 'Career Fair', 'Cultural Event', 'Workshop']
    all_tags = ['Coding', 'Music', 'Cricket', 'Robotics', 'Business', 'Art', 'Debate', 'Gaming', 'AI', 'Networking', 'Photography', 'Volunteering']
    
    event_prefixes = ['Mora', 'Pera', 'Japura', 'Kelaniya', 'Colombo', 'Wayamba', 'Ruhuna', 'AIESEC', 'Rotaract', 'IEEE']
    event_suffixes = ['Fiesta', 'Night', 'Hack', 'Talks', 'Summit', 'CodeFest', 'Bash', 'Symphony', 'Battle', 'Spike']
    
    events = []
    for i in range(1, num_events + 1):
        category = random.choice(categories)
        tags = ", ".join(random.sample(all_tags, k=random.randint(1, 3)))
        
        # Generate Sri Lankan sounding event names
        event_name = f"{random.choice(event_prefixes)} {random.choice(event_suffixes)} 2026"
        if category == 'Hackathon':
            event_name = f"{random.choice(['HackaDev', 'MoraHack', 'CodeSprint', 'ReidHack', 'HackX'])} 2026"
        elif category == 'Musical Show':
            event_name = f"{random.choice(['Baila Night', 'Padura', 'Gimhana', 'MoraBaila', 'Sangeetha Nethgama'])}"
            
        start_date = datetime.now() - timedelta(days=180)
        event_date = start_date + timedelta(days=random.randint(0, 365))
        
        events.append({
            'event_id': f"E{i:03d}",
            'name': event_name,
            'category': category,
            'date': event_date.strftime('%Y-%m-%d'),
            'venue_capacity': random.choice([100, 200, 500, 1000]),
            'tags': tags
        })
    return pd.DataFrame(events)

def generate_attendance(students_df, events_df, num_records=2000):
    student_ids = students_df['student_id'].tolist()
    event_ids = events_df['event_id'].tolist()
    
    attendance = []
    seen_pairs = set()
    
    pos_feedbacks = ["The event was amazing!", "Really enjoyed it.", "Great speakers and organization.", "Loved the vibe.", "Super informative and fun.", "Best event of the year!"]
    neu_feedbacks = ["It was okay.", "Nothing special, but not bad.", "Average experience.", "Decent event.", "Could be better organized."]
    neg_feedbacks = ["Terrible organization.", "Waste of time.", "The audio was really bad.", "Very boring.", "Didn't learn anything."]
    
    while len(attendance) < num_records:
        s_id = random.choice(student_ids)
        e_id = random.choice(event_ids)
        
        if (s_id, e_id) not in seen_pairs:
            seen_pairs.add((s_id, e_id))
            
            # 80% chance they attended if they RSVP'd
            attended = random.choice([1, 1, 1, 1, 0])
            
            # If attended, leave a rating (1-5). If not, rating is null/0.
            rating = random.randint(1, 5) if attended else 0
            
            feedback = ""
            if attended:
                if rating >= 4:
                    feedback = random.choice(pos_feedbacks)
                elif rating == 3:
                    feedback = random.choice(neu_feedbacks)
                else:
                    feedback = random.choice(neg_feedbacks)
            
            attendance.append({
                'student_id': s_id,
                'event_id': e_id,
                'attended': attended,
                'rating': rating,
                'feedback': feedback
            })
            
    return pd.DataFrame(attendance)

if __name__ == "__main__":
    print("Generating Sri Lankan mock data...")
    
    students_df = generate_students(1000)
    events_df = generate_events(150)
    attendance_df = generate_attendance(students_df, events_df, 5000)
    
    # Save to CSV
    students_df.to_csv(os.path.join(DATA_DIR, 'students.csv'), index=False)
    events_df.to_csv(os.path.join(DATA_DIR, 'events.csv'), index=False)
    attendance_df.to_csv(os.path.join(DATA_DIR, 'attendance.csv'), index=False)
    
    print(f"Successfully generated Sri Lankan data and saved to: {DATA_DIR}")
    print(f"- students.csv ({len(students_df)} records)")
    print(f"- events.csv ({len(events_df)} records)")
    print(f"- attendance.csv ({len(attendance_df)} records)")
