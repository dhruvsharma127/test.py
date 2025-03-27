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
