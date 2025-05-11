import json

# JSON 파일을 읽어오기
file_path = 'train_data_final.json'
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# 변환된 데이터를 저장할 리스트
transformed_data = []

for i in range(len(data)):
    item = data[i]
    transformed_item = {
        "messages": [
            {"role": "user", "content": item["question"]},
            {"role": "assistant", "content": item["response"]}
        ]
    }
    transformed_data.append(transformed_item)

# 변환된 데이터를 JSONL 형식으로 저장
output_path = 'transformed_train_data.jsonl'
with open(output_path, 'w', encoding='utf-8') as file:
    for entry in transformed_data:
        json.dump(entry, file)
        file.write('\n')
