import random

def extract_and_write_division_templates(source_path, destination_path):
    """从源文件中提取所有division_template块并写入目标文件。"""
    try:
        with open(source_path, 'r', encoding='utf-8') as src, open(destination_path, 'w', encoding='utf-8') as dest:
            brace_count = 0
            inside_block = False
            for line in src:
                if 'division_template =' in line:
                    inside_block = True
                    brace_count = 0  # Reset brace count for a new block
                if inside_block:
                    if '{' in line:
                        brace_count += line.count('{')
                    if '}' in line:
                        brace_count -= line.count('}')
                    dest.write(line)
                    if brace_count == 0 and inside_block:
                        inside_block = False
                        dest.write('\n')  # 添加空行以便于阅读
                #读到units = {时停止
                if 'units = {' in line:
                    break
        print("所有division_template块已提取并写入到目标文件。")
    except FileNotFoundError:
        print("文件未找到，请检查路径。")

def read_division_template_names(file_path):
    """读取并提取文件中所有保留的division_template的名称。"""
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

def generate_divisions(template_names, location_ids, division_count, destination_path, tag):
    """生成指定数量的division块，并写入目标文件。"""
    # 显示所有的division_template
    print("Available division templates:")
    for idx, name in enumerate(template_names, 1):
        print(f"{idx}. {name}")
    
    # 要求用户选择要排除的模板
    excluded_indexes = input("Enter the numbers of the templates you wish to exclude (separated by spaces, if any): ").split()
    # 将用户输入的索引转换为整数，并从列表中排除这些模板
    excluded_templates = [template_names[int(idx) - 1] for idx in excluded_indexes if idx.isdigit() and 1 <= int(idx) <= len(template_names)]
    # 更新template_names以排除用户选定的模板
    template_names = [name for name in template_names if name not in excluded_templates]

    name_order_dict = {}
    with open(destination_path, 'a', encoding='utf-8') as dest:
        dest.write('units = {\n')  # 添加units块的开始
        for i in range(division_count):
            if not template_names:  # 如果没有剩余的模板可以使用
                print("No templates left to generate divisions. Exiting.")
                break
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
        location = {location}  # Random location
        division_template = "{division_template}"
        start_experience_factor = 0.2
        start_equipment_factor = {start_equipment_factor}
    }}
            '''
            dest.write(division_block)
        dest.write('}\n')  # 添加units块的结束

        # 添加生产内容
        production_content = '''
instant_effect = {
    add_equipment_production = {
        equipment = {
            type = infantry_equipment_1
            creator = "%s"
        }
        requested_factories = 3
        progress = 0.1
        efficiency = 50
    }

    add_equipment_production = {
        equipment = {
            type = support_equipment_1
            creator = "%s" 
        }
        requested_factories = 1
        progress = 0.3
        efficiency = 50
    }
}
        ''' % (tag, tag)
        dest.write(production_content)

# 主程序开始
tag = input("请输入三位的国家TAG：").upper()
source_path = f'F:\\Steam\\steamapps\\common\\Hearts of Iron IV\\history\\units\\{tag}_1936.txt'
destination_path = f'F:\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\World_War_Online\\Hello world\\history\\units\\{tag}_1905.txt'

# 第一步：提取并写入所有division_template块
extract_and_write_division_templates(source_path, destination_path)

# 等待用户筛选模板后继续
input("完成模板筛选后请按回车继续...")

# 第二步：读取筛选后的模板名称
template_names = read_division_template_names(destination_path)

# 获取用户输入的其他信息
division_count = int(input("请输入需要生成的师的数量："))
location_ids = input("请输入地块id，用空格分隔：").split()

# 第三步：生成division块并写入文件
generate_divisions(template_names, location_ids, division_count, destination_path, tag)

print(f"{division_count}个师的部署文件已生成至{destination_path}")
