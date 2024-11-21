import os

def clean_labels(label_dir):
    for file in os.listdir(label_dir):
        if file.endswith('.txt'):
            filepath = os.path.join(label_dir, file)
            cleaned_lines = set()  # 用集合去重
            with open(filepath, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) == 5:
                        class_id, x_center, y_center, width, height = map(float, parts)
                        if 0 <= class_id < 10 and 0 <= x_center <= 1 and 0 <= y_center <= 1 and 0 <= width <= 1 and 0 <= height <= 1:
                            cleaned_lines.add(line.strip())
            with open(filepath, 'w') as f:
                f.write('\n'.join(cleaned_lines))

label_dir = '/Users/leojackasher/PycharmProjects/PythonProject2/data/train/labels'
clean_labels(label_dir)