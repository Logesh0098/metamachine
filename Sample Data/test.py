import cv2
import os
import numpy as np

# ✅ Define the answer key (example with 5 questions, 4 options each)
answer_key = {
    1: "B",
    2: "D",
    3: "A",
    4: "C",
    5: "B"
}

# ✅ Path to dataset folder
dataset_path = "Set A"

# ✅ Predefined bubble positions (example format)
# question_number: { "A": (x, y, w, h), "B": (x, y, w, h), ... }
bubble_positions = {
    1: {"A": (50, 100, 30, 30), "B": (100, 100, 30, 30), "C": (150, 100, 30, 30), "D": (200, 100, 30, 30)},
    2: {"A": (50, 200, 30, 30), "B": (100, 200, 30, 30), "C": (150, 200, 30, 30), "D": (200, 200, 30, 30)},
    3: {"A": (50, 300, 30, 30), "B": (100, 300, 30, 30), "C": (150, 300, 30, 30), "D": (200, 300, 30, 30)},
    4: {"A": (50, 400, 30, 30), "B": (100, 400, 30, 30), "C": (150, 400, 30, 30), "D": (200, 400, 30, 30)},
    5: {"A": (50, 500, 30, 30), "B": (100, 500, 30, 30), "C": (150, 500, 30, 30), "D": (200, 500, 30, 30)},
}

# ✅ Extract answers based on bubble darkness
def extract_answers(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)

    detected_answers = {}

    for q_no, options in bubble_positions.items():
        darkness = {}

        for option, (x, y, w, h) in options.items():
            roi = thresh[y:y+h, x:x+w]  # crop bubble region
            total_pixels = w * h
            filled_pixels = cv2.countNonZero(roi)
            fill_ratio = filled_pixels / float(total_pixels)

            darkness[option] = fill_ratio

        # Pick the darkest bubble (highest ratio)
        marked = max(darkness, key=darkness.get)

        # Apply a threshold so random noise doesn’t count
        if darkness[marked] > 0.5:  # means bubble is at least 50% filled
            detected_answers[q_no] = marked

    return detected_answers

# ✅ Grade student
def grade_student(detected_answers, answer_key):
    score = 0
    for q_no, correct_ans in answer_key.items():
        if q_no in detected_answers and detected_answers[q_no] == correct_ans:
            score += 1
    return score

# ✅ Process each student image
for file in os.listdir(dataset_path):
    if file.endswith(".jpg") or file.endswith(".png"):
        path = os.path.join(dataset_path, file)
        student_answers = extract_answers(path)
        score = grade_student(student_answers, answer_key)

        print(f"Student: {file} | Answers: {student_answers} | Score: {score}/{len(answer_key)}")
