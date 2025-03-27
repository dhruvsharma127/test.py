import pandas as pd

data = {
    "student_id": [101, 101, 101, 101, 101,
                   102, 102, 102, 102,
                   103, 103, 103, 103, 103,
                   104, 104, 104, 104, 104],
    "attendance_date": ["2024-03-01", "2024-03-02", "2024-03-03", "2024-03-04", "2024-03-05",
                        "2024-03-02", "2024-03-03", "2024-03-04", "2024-03-05",
                        "2024-03-05", "2024-03-06", "2024-03-07", "2024-03-08", "2024-03-09",
                        "2024-03-01", "2024-03-02", "2024-03-03", "2024-03-04", "2024-03-05"],
    "status": ["Absent", "Absent", "Absent", "Absent", "Present",
               "Absent", "Absent", "Absent", "Absent",
               "Absent", "Absent", "Absent", "Absent", "Absent",
               "Present", "Present", "Absent", "Present", "Present"]
}

df = pd.DataFrame(data)
df['attendance_date'] = pd.to_datetime(df['attendance_date'])


def find_absent_streaks(df, threshold=3):
    streaks = []

    for student in df['student_id'].unique():
        student_data = df[df['student_id'] == student].sort_values('attendance_date')
        streak_start = None
        streak_count = 0

        for i in range(len(student_data)):
            if student_data.iloc[i]['status'] == "Absent":
                if streak_start is None:
                    streak_start = student_data.iloc[i]['attendance_date']
                streak_count += 1
            else:
                if streak_count > threshold:
                    streaks.append({
                        "student_id": student,
                        "absence_start_date": streak_start,
                        "absence_end_date": student_data.iloc[i - 1]['attendance_date'],
                        "total_absent_days": streak_count
                    })
                streak_start = None
                streak_count = 0

        if streak_count > threshold:
            streaks.append({
                "student_id": student,
                "absence_start_date": streak_start,
                "absence_end_date": student_data.iloc[-1]['attendance_date'],
                "total_absent_days": streak_count
            })

    return pd.DataFrame(streaks)

absent_streaks = find_absent_streaks(df)
print(absent_streaks)

parent_data = {
    "student_id": [101, 102, 103, 104, 105],
    "student_name": ["Alice Johnson", "Bob Smith", "Charlie Brown", "David Lee", "Eva White"],
    "parent_email": ["alice_parent@example.com", "bob_parent@example.com", 
                     "invalid_email.com", "invalid_email.com", "eva_white@example.com"]
}

parent_df = pd.DataFrame(parent_data)

merged_df = df.merge(parent_df, on="student_id", how="left")

print(merged_df)

import re

def is_valid_email(email):
    pattern = r'^[a-zA-Z_][a-zA-Z0-9_.]*@[a-zA-Z]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

parent_df['is_valid_email'] = parent_df['parent_email'].apply(is_valid_email)

print(parent_df[['student_id', 'student_name', 'parent_email', 'is_valid_email']])

merged_df = df.merge(parent_df, on="student_id", how="left")
absent_streaks = find_absent_streaks(df)
final_df = absent_streaks.merge(parent_df, on="student_id", how="left")

def is_valid_email(email):
    pattern = r'^[a-zA-Z_][a-zA-Z0-9_.]*@[a-zA-Z]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

final_df['email'] = final_df['parent_email'].apply(lambda x: x if is_valid_email(x) else '')

def generate_message(row):
    if row['email']:
        return (f"Dear Parent, your child {row['student_name']} was absent from "
                f"{row['absence_start_date'].strftime('%Y-%m-%d')} to {row['absence_end_date'].strftime('%Y-%m-%d')} "
                f"for {row['total_absent_days']} days. Please ensure their attendance improves.")
    return ''

final_df['msg'] = final_df.apply(generate_message, axis=1)
output_df = final_df[['student_id', 'student_name', 'email', 'msg']]
print(output_df)
