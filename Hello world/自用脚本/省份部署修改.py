import os
import shutil
print("！！！首次运行前请确保已修改源目录和目标目录路径。！！！")
#定义源目录和目标目录路径,你需要修改这里两个路径
source_dir = r"F:\Steam\steamapps\common\Hearts of Iron IV\history\states" #这里是你的HOI4安装目录
target_dir = r"F:\Documents\Paradox Interactive\Hearts of Iron IV\mod\xxx\history\states" #这里是你的mod目录，xxx是你的mod名字

# 确保目标目录存在
os.makedirs(target_dir, exist_ok=True)

# 用户输入
new_owner = input("请输入修改后的省份归属（三个字母）: ").upper()
is_core = input("是否为核心领土？(回车为是，n为否): ").strip().lower() != 'n'

def modify_province_file(file_path, province_id):
    # 修改文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.readlines()

    with open(file_path, 'w', encoding='utf-8') as file:
        for line in content:
            if line.strip().startswith("owner ="):
                file.write(f"owner = {new_owner}\n")
                if is_core:
                    file.write(f"add_core_of = {new_owner}\n")
            else:
                file.write(line)

while True:
    province_id = input("请输入省份ID（输入'q'退出）: ").strip()
    if province_id.lower() == 'q':
        break

    target_file_path = os.path.join(target_dir, f"{province_id}-*.txt")
    file_found = False

    # 检查目标目录中是否已存在对应的省份文件
    for file in os.listdir(target_dir):
        if file.startswith(province_id + "-"):
            target_file_path = os.path.join(target_dir, file)
            modify_province_file(target_file_path, province_id)
            print(f"省份{province_id}已在目标目录中更新。")
            file_found = True
            break

    # 如果目标目录中不存在，尝试从源目录复制
    if not file_found:
        for file in os.listdir(source_dir):
            if file.startswith(province_id + "-"):
                source_file_path = os.path.join(source_dir, file)
                target_file_path = os.path.join(target_dir, file)
                shutil.copy(source_file_path, target_file_path)
                modify_province_file(target_file_path, province_id)
                print(f"省份{province_id}已从源目录复制并更新。")
                break
        else:
            print("未找到对应的省份文件，请重试。")
