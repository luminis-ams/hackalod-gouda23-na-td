from copy import deepcopy

import pandas as pd
import json
from pathlib import Path


allowed_structures = [
    'index_military',
    'name',
    'family_data',
    'muster_data',
    'campaign_data',
    'comments',
]




def preprocess(element, prefix=''):
    prefix_add = '  '
    if isinstance(element, dict):
        if 'structure' in element:
            print(prefix + 'structure: ' + element['structure'])
        if 'text' in element:
            print(prefix + element['text'])
        if 'region_text' in element:
            print(prefix + 'region_text: ' + element['region_text'])
        if 'row_surname' in element:
            print(prefix + 'row_surname: ' + element['row_surname'])
        if 'row_name' in element:
            print(prefix + 'row_name: ' + element['row_name'])

        for key, value in element.items():
            preprocess(value, prefix + prefix_add + '- ')
    elif isinstance(element, list):
        # print('parent:')
        for item in element:
            preprocess(item, prefix + prefix_add)
    else:
        pass


def extract_entities(items: list):
    output = []
    cur_entity_type = None
    cur_entity_content = None

    # print(f'extract_entities: {items}')

    for item in items:
        if isinstance(item, dict):
            if 'key' in item and item['key'] == 'structure':
                if cur_entity_type:
                    output.append({
                        'type': cur_entity_type,
                        'content': cur_entity_content
                    })
                cur_entity_type = item['value']
                cur_entity_content = []
            else:
                if cur_entity_type:
                    cur_entity_content.append(item)
                else:
                    output.append(item)
        elif cur_entity_type:
            cur_entity_content.append(item)
        else:
            output.append(item)

    if cur_entity_type:
        output.append({
            'entity_type': cur_entity_type,
            'content': cur_entity_content
        })

    return output


def preprocess_v2(element):
    if isinstance(element, dict):
        output = []

        if 'structure' in element:
            output.append({
                'key': 'structure',
                'value': element['structure']
            })
        if 'text' in element:
            output.append({
                'key': 'text',
                'value': element['text']
            })
        if 'region_text' in element:
            output.append({
                'key': 'region_text',
                'value': element['region_text']
            })
        if 'row_surname' in element:
            output.append({
                'key': 'row_surname',
                'value': element['row_surname']
            })
        if 'row_name' in element:
            output.append({
                'key': 'row_name',
                'value': element['row_name']
            })

        children = []
        for key, value in element.items():
            if child := preprocess_v2(value):
                children.append(child)
        if children:
            if all([isinstance(c, str) for c in children]):
                children = ' '.join(children)
                output.append({
                    'key': 'child_text',
                    'value': children
                })
            else:
                children = extract_entities(children)
                output.append({
                    'key': 'children',
                    'value': children
                })

        if len(output) == 1 and output[0]['key'] == 'text':
            output = output[0]['value']
        else:
            output = extract_entities(output)
    elif isinstance(element, list):
        output = []
        for item in element:
            if child := preprocess_v2(item):
                output.append(child)

        output = extract_entities(output)
    else:
        output = None
    return output


def flatten_me_like_a_bus(data):
    if isinstance(data, dict):
        if 'entity_type' in data:
            data['content'] = flatten_me_like_a_bus(data['content'])
        elif 'key' in data and data['key'] == 'children':
            data['value'] = flatten_me_like_a_bus(data['value'])

            if isinstance(data['value'], dict) and data['value'].get('key', None) == 'children':
                data['value'] = data['value']['value']

            data = data['value']
        elif 'key' in data and data['key'] == 'child_text':
            data = data['value']
        elif 'key' in data and data['key'] == 'region_text':
            data = data['value']
        else:
            # data['value'] = flatten_me_like_a_bus(data['value'])
            data = f'{data["key"]}: {flatten_me_like_a_bus(data["value"])}'
    elif isinstance(data, list):
        data = [flatten_me_like_a_bus(item) for item in data]
        if len(data) == 1 and isinstance(data[0], list | str):
            data = data[0]
    elif isinstance(data, str):
        pass
    return data


def clean_me_like_a_firehose(data):
    if isinstance(data, list):
        data = [clean_me_like_a_firehose(item) for item in data]
        data_new = []
        already_seen = set()
        for item in data:
            if isinstance(item, dict | list):
                data_new.append(item)
                continue

            if item in already_seen:
                continue
            already_seen.add(item)
            data_new.append(item)

        data = data_new
    elif isinstance(data, dict):
        if 'entity_type' in data:
            entity_type = data['entity_type']
            value = None
            if entity_type in {'comments', 'campaign_data', 'muster_data', 'index', 'family_data'}:
                value = data['content'][1:]
            else:
                value = data['content']

            data = {
                'entity': entity_type,
                'value': value
            }
    elif isinstance(data, str):
        data = data.strip()
    else:
        pass
    return data


def pannekoek(data):
    output = []

    def inner_pannekoek(data):
        if isinstance(data, dict):
            output.append(data)
        elif isinstance(data, list):
            for item in data:
                inner_pannekoek(item)
        else:
            pass

    inner_pannekoek(data)

    title = None
    people = []
    events = []

    for entity in output:
        if entity['entity'] in ['campaign_data', 'muster_data']:
            value = [entity['value']] if isinstance(entity['value'], str) else entity['value']
            entity['value'] = [v for v in entity['value'] if v]
            if len(entity['value']) == 0:
                continue
            events.append(value)
        elif entity['entity'] in [ 'family_data']:
            value = [entity['value']] if isinstance(entity['value'], str) else entity['value']
            entity['value'] = [v for v in entity['value'] if v]
            if len(entity['value']) == 0:
                continue
            people.append(value)
        elif entity['entity'] in ['index_military']:
            title = entity['value']
        else:
            pass

    return {
        'title': title,
        'people': people,
        'events': events
    }



def main(data):
    helloz = preprocess_v2(deepcopy(data))
    flattened_data = flatten_me_like_a_bus(deepcopy(helloz))
    cleaned_data = clean_me_like_a_firehose(deepcopy(flattened_data))
    result = pannekoek(deepcopy(cleaned_data))

    return result


for file in Path('../../data/suppleties').glob('*.json'):
    with open(file, 'r') as f:
        data = json.load(f)
        result = main(data)

    if not result or not result['people'] or not result['events']:
        continue
    print('Writing')
    with Path(f'../../data/suppleties_cleaned/{file.name}').open('w') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
