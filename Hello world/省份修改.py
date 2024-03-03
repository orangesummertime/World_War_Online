import os
import shutil

# 定义源目录和目标目录路径
source_dir = r"F:\Steam\steamapps\common\Hearts of Iron IV\history\states"
target_dir = r"F:\Documents\Paradox Interactive\Hearts of Iron IV\mod\World_War_Online\Hello world\history\states"
history_file_path = r"F:\Documents\Paradox Interactive\Hearts of Iron IV\mod\World_War_Online\Hello world\省份修改历史.txt"

# 确保目标目录存在
os.makedirs(target_dir, exist_ok=True)

# 用户输入
new_owner = input("请输入修改后的省份归属（三个字母）: ").upper()
is_core = input("是否为核心领土？(回车为是，n为否): ").strip().lower() != 'n'

while True:
    province_id = input("请输入省份ID（输入'q'退出）: ").strip()
    if province_id.lower() == 'q':
        break

    # 构建文件名和路径
    file_name = f"{province_id}-*.txt"
    for file in os.listdir(source_dir):
        if file.startswith(province_id + "-"):
            source_file_path = os.path.join(source_dir, file)
            target_file_path = os.path.join(target_dir, file)

            # 复制文件
            shutil.copy(source_file_path, target_file_path)

            # 修改文件内容
            with open(target_file_path, 'r', encoding='utf-8') as file:
                content = file.readlines()

            with open(target_file_path, 'w', encoding='utf-8') as file:
                for line in content:
                    if line.strip().startswith("owner ="):
                        file.write(f"owner = {new_owner}\n")
                        if is_core:
                            file.write(f"add_core_of = {new_owner}\n")
                    else:
                        file.write(line)

            # 记录到省份修改历史文件
            with open(history_file_path, 'a', encoding='utf-8') as history_file:
                history_file.write(f"{file}\n")

            print(f"省份{province_id}已更新。")
            break
    else:
        print("未找到对应的省份文件，请重试。")
