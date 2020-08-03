import json
with open("data/quiz.json") as json_file:
    json_data = json.load(json_file)

q = json_data['quiz'].items()

for x, y in q:
    print(f"Question {x}: {y['question']}")
    for op in y['options']:
        print(f"    {op}")
    print()