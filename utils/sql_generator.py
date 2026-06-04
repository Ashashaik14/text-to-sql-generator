def generate_sql(user_text):
    # For now simple rule-based (you can replace with OpenAI later)

    if "student" in user_text.lower():
        return "SELECT * FROM students;"

    if "marks above" in user_text.lower():
        return "SELECT * FROM students WHERE marks > 75;"

    return "SELECT * FROM table WHERE condition;"