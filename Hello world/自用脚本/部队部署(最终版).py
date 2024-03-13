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
                        dest.write('\n')  # Ensure separation between templates for readability
                if 'units = {' in line:
                    break
        print("所有division_template块已提取并写入到目标文件。请进行必要的修改。")
    except FileNotFoundError:
        print("文件未找到，请检查路径。")
    input("请在文件中完成模板修改后按回车继续...")

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

def filter_out_excluded_templates(template_names):
    print("Available division templates:")
    for idx, name in enumerate(template_names, start=1):
        print(f"{idx}. {name}")
    excluded_indexes = input("输入你希望排除的模板编号，用空格分隔（如果没有，请直接回车）: ").split()
    excluded_templates = set(template_names[int(idx) - 1] for idx in excluded_indexes if idx.isdigit() and 1 <= int(idx) <= len(template_names))
    return [name for name in template_names if name not in excluded_templates]

def find_victory_points_paths(root_dir, tag, excluded_states):
    victory_points_ids = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            state_id = file.split("-")[0]
            if state_id in excluded_states:
                continue
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
                                if parts and parts[0].isdigit():
                                    vp_id = parts[0]
                                    victory_points_ids.append(vp_id)
                            start = content.find("victory_points = {", end)
    return victory_points_ids

def generate_divisions(template_names, location_ids, division_count, destination_path, tag, is_first_section):
    name_order_dict = {}
    with open(destination_path, 'a', encoding='utf-8') as dest:
        dest.write('units = {\n')
        for i in range(division_count):
            if not template_names:
                print("No templates left to generate divisions. Exiting.")
                break
            division_template = random.choice(template_names) if location_ids else input("Choose a division template from the list: ")
            name_order = name_order_dict.get(division_template, 0) + 1
            name_order_dict[division_template] = name_order
            location = random.choice(location_ids) if location_ids else input("Enter the location ID for this division: ")
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

def add_production_content(destination_path, tag):
    production_content = f'''
instant_effect = {{
    add_equipment_production = {{
        equipment = {{
            type = infantry_equipment_1
            creator = "{tag}"
        }}
        requested_factories = 3
        progress = 0.1
        efficiency = 50
    }}

    add_equipment_production = {{
        equipment = {{
            type = support_equipment_1
            creator = "{tag}" 
        }}
        requested_factories = 1
        progress = 0.3
        efficiency = 50
    }}
}}
    '''
    with open(destination_path, 'a', encoding='utf-8') as file:
        file.write(production_content)

def main():
    print("这个脚本不需要任何外部库，只需要你的HOI4安装目录和mod目录，首次运行前需要手动修改此脚本！（要改的地方在这行print代码下面，留了注释的）")
    tag = input("请输入三位的国家TAG：").upper()
    source_path = f"F:\\Steam\\steamapps\\common\\Hearts of Iron IV\\history\\units\\{tag}_1936.txt" #这里是你的HOI4安装目录
    destination_path = f"F:\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\xxx\\history\\units\\{tag}_1905.txt"#这里是你的mod目录，xxx是你的mod名字，1905是你的mod开始时间
    
    # 提取并暂停等待用户手动修改
    extract_and_write_division_templates(source_path, destination_path)
    
    # 读取并允许用户排除模板
    template_names = read_division_template_names(destination_path)
    template_names = filter_out_excluded_templates(template_names)
    
    auto_deploy = input("是否要自动在胜利点部署？(y/n): ").lower() == 'y'
    if auto_deploy:
        excluded_states_input = input("请输入需要跳过的state id，用空格分隔（如果没有请直接回车）: ")
        excluded_states = excluded_states_input.split() if excluded_states_input else []
        vp_ids_hoi4 = find_victory_points_paths(r"F:\Steam\steamapps\common\Hearts of Iron IV\history\states", tag, excluded_states)
        vp_ids_mod = find_victory_points_paths(r"F:\Documents\Paradox Interactive\Hearts of Iron IV\mod\World_War_Online\Hello world\history\states", tag, excluded_states)
        location_ids = vp_ids_hoi4 + vp_ids_mod
        division_count = int(input("请输入自动部署的部队数量："))
        generate_divisions(template_names, location_ids, division_count, destination_path, tag, True)

    manual_deploy = input("是否要继续手动部署部队？(y/n): ").lower() == 'y'
    if manual_deploy:
        division_count_manual = int(input("请输入手动部署的部队数量："))
        location_ids_manual = input("请输入地块id，用空格分隔：").split()
        generate_divisions(template_names, location_ids_manual, division_count_manual, destination_path, tag, False)

    add_production_content(destination_path, tag)

if __name__ == "__main__":
    main()
