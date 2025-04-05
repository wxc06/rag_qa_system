
import json
import re
from collections import defaultdict

def convert_webfaq_to_json(txt_path, output_path='data/split_chunks.json', lang_filter='en'):
    '''
    将WebFAQ中的RDF格式转换为问答对结构
    参数:
        txt_path: 输入原始RDF格式的路径
        output_path: 输出JSON文件路径（供系统加载）
        lang_filter: 当前仅处理英文
    '''
    with open(txt_path, ' 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 数据结构解析
    qid2text = defaultdict(dict)
    q_map = {}  # Question ID -> {'question': ..., 'answer': ..., 'source': ...}

    for line in lines:
        parts = line.strip().split(' ', 3)
        if len(parts) < 4:
            continue
        subj, pred, obj, url = parts
        subj = subj.strip()
        pred = pred.strip().strip('<>').split('/')[-1]
        obj = obj.strip().strip('<>"')
        url = url.strip()

        # 捕获问题内容
        if pred == 'name':
            qid2text[subj]['question'] = obj
            qid2text[subj]['source'] = url
        # 捕获回答内容
        elif pred == 'text':
            qid2text[subj]['answer'] = obj

    # 过滤有效问答对
    results = []
    for item in qid2text.values():
        if 'question' in item and 'answer' in item:
            # 粗略判断英文
            if re.search(r'[a-zA-Z]{5,}', item['question']) and re.search(r'[a-zA-Z]{5,}', item['answer']):
                results.append({
                    'question': item['question'],
                    'answer': item['answer'],
                    'source': item.get('source', '')
                })

    print(f"共解析出有效问答对：{len(results)}")
    # 保存为JSON
    Path(output_path).parent.mkdir(exist_ok=True, parents=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    # 
    convert_webfaq_to_json('data/FAQPage_sample.txt')
