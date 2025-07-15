from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import random
import os
from urllib.parse import quote


app = Flask(__name__)

# Session configuration
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

patch_version = "15.13.1"

# 環境変数から秘密のパスワードを取得（本番環境で設定）
SECRET_PASSWORD = os.environ.get('SECRET_PASSWORD', '')
SECRET_PASSWORD_HASH = generate_password_hash(SECRET_PASSWORD) if SECRET_PASSWORD else None

def get_items_data():
    url = f"https://ddragon.leagueoflegends.com/cdn/{patch_version}/data/ja_JP/item.json"
    response = requests.get(url)
    return response.json()

def build_item_tree(item_id, items):
    item = items.get(item_id)
    if item is None or item.get('requiredAlly') == 'Ornn':
        return None
    node = {
        'id': item_id,
        'name': item['name'],
        'parents': [],
        'gold': item['gold']['total'],
        'image': item['image']['full'],
        'image_url': f"https://ddragon.leagueoflegends.com/cdn/{patch_version}/img/item/{item['image']['full']}",  # 画像URLを追加
        'tags': item.get('tags', [])
    }
    return node

def get_tree_item_names(tree, trees):
    if tree is None:
        return []
    names = [tree['name']]
    for parent_id in tree['parents']:
        names.extend(get_tree_item_names(trees[parent_id], trees))
    return names


def check_answers(selected_item_names, tree_item_names, user_answers):
    correct_answers = set([name for name in selected_item_names if name in tree_item_names])
    if correct_answers == set(user_answers):
        return f"oooo(*^▽^*)oooo"
    else:
        return f"(´・ω・`)"

def filter_items(all_items):
    map_filtered_items = {item_id: item for item_id, item in all_items.items() if item.get('maps', {}).get('11', False) and not all(item.get('maps', {}).get(map_id, False) for map_id in ['11', '12', '21', '30'])}
    
    target_tags = ['Consumable', 'Trinket', 'Boots', 'Jungle', 'Lane']
    exclude_item_names = ['ロング ソード']
    tag_filtered_items = {item_id: item for item_id, item in all_items.items() if any(tag in item.get('tags', []) for tag in target_tags) and item['name'] not in exclude_item_names}
    
    final_filtered_items = {item_id: item for item_id, item in map_filtered_items.items() if item_id not in tag_filtered_items}
    
    exclude_ids = ['6693', '6673', '4641', '4637', '1516', '1517', '1518', '1519']
    last_final_filtered_items = {item_id: item for item_id, item in final_filtered_items.items() if item_id not in exclude_ids}
    
    return last_final_filtered_items

def connect_parents(items, trees):
    for item_id, item in items.items():
        if 'from' in item:
            for parent_id in item['from']:
                if parent_id in trees:
                    trees[item_id].setdefault('children', []).append(parent_id)
                    trees[parent_id]['parents'].append(item_id)

def get_immediate_family(item_id, trees):
    item_tree = trees.get(item_id)
    if item_tree is None:
        return []

    family = []
    if 'parents' in item_tree:
        family.extend(item_tree['parents'])
    if 'children' in item_tree:
        family.extend(item_tree['children'])
    return family

def get_extended_family(item_id, trees, items):
    immediate_family = get_immediate_family(item_id, trees)
    extended_family = set(immediate_family)  # Use a set to avoid duplicates

    for family_member_id in immediate_family:
        family_member_family = get_immediate_family(family_member_id, trees)
        for family_member_family_id in family_member_family:
            family_member_family_member_family = get_immediate_family(family_member_family_id, trees)
            extended_family.update(family_member_family_member_family)

    # Filter out items with 'gold' less than 500
    extended_family = [family_id for family_id in extended_family if items[family_id]['gold']['total'] >= 500]

    return extended_family

@app.route('/')
def index():
    session.clear()
    return render_template('index.html', patch_version=patch_version)

@app.route('/quiz_a', methods=['GET', 'POST'])
def quiz_a():
    submitted = False
    result = None
    is_correct = None
    sentakusi = 10
    consecutive_correct_answers = session.get('consecutive_correct_answers', 0)  # 連続正解回数をセッションから取得
    previous_consecutive_correct_answers = session.get('previous_consecutive_correct_answers', 0)

    if request.method == 'POST':
        options = session.get('options')
        answers = session.get('correct_answers')
        user_answers = request.form.getlist('answer')
        result = check_answers(options, answers, user_answers)
        session['result'] = result
        submitted = True
        answer_marks = [{ 'name': name, 'is_correct': (name in answers), 'checked': (name in user_answers) } for name in options]
        
        # 連続正解回数の更新
        if session['result'] == "oooo(*^▽^*)oooo":
            consecutive_correct_answers += 1
            is_correct = True
        else:
            consecutive_correct_answers = 0
            previous_consecutive_correct_answers = session.get('consecutive_correct_answers', 0)
            is_correct = False

        session['consecutive_correct_answers'] = consecutive_correct_answers  # セッションに保存
        session['previous_consecutive_correct_answers'] = previous_consecutive_correct_answers
    else:
        session['previous_consecutive_correct_answers'] = 0
        data = get_items_data()
        all_items = {item_id: item for item_id, item in data['data'].items() if item.get('requiredAlly') != 'Ornn'}
        filtered_items = filter_items(all_items)
        all_trees = {item_id: build_item_tree(item_id, filtered_items) for item_id in filtered_items}
        connect_parents(filtered_items, all_trees)

        large_trees = {item_id: tree for item_id, tree in all_trees.items() if tree and len(get_tree_item_names(tree, all_trees)) >= 5}
        session['item_id'] = random.choice(list(large_trees.keys()))
        extended_family = get_extended_family(session.get('item_id'), all_trees, all_items)
        extended_family_names = [filtered_items[family_id]['name'] for family_id in extended_family if family_id != session.get('item_id')]
        session['options'] = random.sample(extended_family_names, min(sentakusi, len(extended_family_names)))
        session['item_tree'] = large_trees[session.get('item_id')]
        session['correct_answers'] = get_tree_item_names(session.get('item_tree'), all_trees)[1:]
        answer_marks = [{ 'name': name, 'is_correct': False, 'checked': False } for name in session.get('options')]

    result = session.pop('result', None)

    return render_template('quiz_a.html', 
                           result=result, 
                           submitted=submitted, 
                           is_correct=is_correct,
                           item=session.get('item_tree'),
                           answer_marks=answer_marks, 
                           consecutive_correct_answers=consecutive_correct_answers, 
                           previous_consecutive_correct_answers=previous_consecutive_correct_answers,
                           patch_version=patch_version)

@app.route('/quiz_b', methods=['GET', 'POST'])
def quiz_b():
    submitted = False
    result = None
    is_correct = None
    consecutive_correct_answers = session.get('consecutive_correct_answers', 0)  # 連続正解回数をセッションから取得
    previous_consecutive_correct_answers = session.get('previous_consecutive_correct_answers', 0)

    if request.method == 'POST':
        selected_item = session.get('selected_item')
        if not request.form.get('price'):
            user_answer = 0
        else:
            user_answer = int(request.form.get('price'))
        
        # 秘密の機能（環境変数が設定されている場合のみ有効）
        if SECRET_PASSWORD_HASH and check_password_hash(SECRET_PASSWORD_HASH, str(user_answer)):
            session['authenticated'] = True
            return redirect(url_for('secret'))
        
        correct_answer = session.get('correct_price')
        submitted = True
        if user_answer == correct_answer:
            result = "正解です！"
            consecutive_correct_answers += 1
            is_correct = True
        else:
            result = f"不正解です。正解は {correct_answer} です。"
            consecutive_correct_answers = 0
            previous_consecutive_correct_answers = session.get('consecutive_correct_answers', 0)
            is_correct = False

        session['result'] = result
        session['consecutive_correct_answers'] = consecutive_correct_answers  # セッションに保存
        session['previous_consecutive_correct_answers'] = previous_consecutive_correct_answers
    else:
        session['previous_consecutive_correct_answers'] = 0
        data = get_items_data()
        items_dict = {item_id: item for item_id, item in data['data'].items() if item.get('requiredAlly') != 'Ornn'}
        filtered_items_dict = filter_items(items_dict)
        filtered_items_list = list(filtered_items_dict.values())
        selected_item = random.choice(filtered_items_list)
        session['selected_item'] = selected_item
        session['correct_price'] = selected_item['gold']['total']

    result = session.pop('result', None)

    return render_template('quiz_b.html', 
                           item=selected_item, 
                           result=result, 
                           submitted=submitted,
                           is_correct=is_correct,
                           consecutive_correct_answers=consecutive_correct_answers, 
                           previous_consecutive_correct_answers=previous_consecutive_correct_answers,
                           patch_version=patch_version)  

@app.route('/next_question_a', methods=['GET'])
def next_question_a():
    session.pop('submitted', None)
    session.pop('result', None)
    return redirect(url_for('quiz_a'))

@app.route('/next_question_b', methods=['GET'])
def next_question_b():
    session.pop('submitted', None)
    session.pop('result', None)
    return redirect(url_for('quiz_b'))

@app.route('/algorithm')
def algorithm():
    return render_template('algorithm.html', patch_version=patch_version)

@app.route('/secret')
def secret():
    if not session.get('authenticated'):
        return redirect(url_for('index'))
    return render_template('secret.html', patch_version=patch_version)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # 環境変数PORTからポート番号を取得
    app.run(host='0.0.0.0', port=port, debug=True)
