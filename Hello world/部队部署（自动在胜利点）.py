import os
import random

def extract_and_write_division_templates(source_path, destination_path):
    try:
        with open(source_path, 'r', encoding='utf-8') as src, open(destination_path, 'w', encoding='utf-8') as dest:
            brace_count = 0
            inside_block = False
            for line in src:
                if 'division_template =' in line:
                    inside_block = True
                    brace_count = 0
                if inside_block:
                    if '{' in line:
                        brace_count += line.count('{')
                    if '}' in line:
                        brace_count -= line.count('}')
                    dest.write(line)
                    if brace_count == 0 and inside_block:
                        inside_block = False
                        dest.write('\n')
        print("所有division_template块已提取并写入到目标文件。")
    except FileNotFoundError:
        print("文件未找到，请检查路径。")

def read_division_template_names(file_path):
    template_names = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        for line in lines:
            if 'name =' in line:
                start_index = line.find('"') + 1
                end_index = line.find('"', start_index)
                name = line[start_index:end_index]
                template_names.append(name)
    except FileNotFoundError:
        print("文件未找到，请检查路径。")
    return template_names

def find_victory_points_paths(root_dir, tag):
    victory_points_ids = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if f"owner = {tag}" in content:
                        start = content.find("victory_points = {")
                        while start != -1:
                            start = content.find("{", start) + 1
                            end = content.find("}", start)
                            block_content = content[start:end].strip()
                            if block_content:
                                parts = block_content.split()
                                # 检查第一个元素是否为数字
                                if parts and parts[0].isdigit():
                                    vp_id = parts[0]
                                    victory_points_ids.append(vp_id)
                            start = content.find("victory_points = {", end)
    return victory_points_ids

def generate_divisions(template_names, division_count, destination_path, tag):
    vp_ids_hoi4 = find_victory_points_paths(r"F:\Steam\steamapps\common\Hearts of Iron IV\history\states", tag)
    vp_ids_mod = find_victory_points_paths(r"F:\Documents\Paradox Interactive\Hearts of Iron IV\mod\World_War_Online\Hello world\history\states", tag)
    location_ids = vp_ids_hoi4 + vp_ids_mod
    if not location_ids:
        print("未找到符合要求的地块id。")
        return
    name_order_dict = {}
    with open(destination_path, 'a', encoding='utf-8') as dest:
        dest.write('units = {\n')
        for i in range(division_count):
            division_template = random.choice(template_names)
            name_order = name_order_dict.get(division_template, 0) + 1
            name_order_dict[division_template] = name_order
            location = random.choice(location_ids)
            start_equipment_factor = round(random.uniform(0.3, 0.9), 1)
            division_block = f'''
    division= {{
        division_name = {{
            is_name_ordered = yes
            name_order = {name_order}
        }}
        location = {location}
        division_template = "{division_template}"
        start_experience_factor = 0.2
        start_equipment_factor = {start_equipment_factor}
    }}
            '''
            dest.write(division_block)
        dest.write('}\n')

        # Append production content etc.

tag = input("请输入三位的国家TAG：").upper()
source_path = f'F:\\Steam\\steamapps\\common\\Hearts of Iron IV\\history\\units\\{tag}_1936.txt'
destination_path = f'F:\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\World_War_Online\\Hello world\\history\\units\\{tag}_1905.txt'

extract_and_write_division_templates(source_path, destination_path)
input("完成模板筛选后请按回车继续...")

template_names = read_division_template_names(destination_path)
division_count = int(input("请输入需要生成的师的数量："))

generate_divisions(template_names, division_count, destination_path, tag)

print(f"{division_count}个师的部署文件已生成至{destination_path}")
