import os
import glob
from wand.image import Image

def get_custom_filename(default_name, extension, replace_space=True):
    custom_name = input("请输入生成文件的名字（回车保持不变）: ").strip()
    if replace_space:
        custom_name = custom_name.replace(' ', '_')
    if custom_name:
        return custom_name + extension
    else:
        return default_name + extension

def save_flag_versions(filename, custom_name):
    resolutions = [(82, 52), (41, 26), (10, 7)]
    directories = ["flags", "flags/medium", "flags/small"]
    for res, dir_name in zip(resolutions, directories):
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        with Image(filename=filename) as img:
            img.resize(*res)
            img.flip()  # 上下翻转图像
            new_filename = os.path.join(dir_name, custom_name + '.tga')
            img.save(filename=new_filename)
            print(f"图像已保存为: {new_filename}")

script_dir = os.path.dirname(os.path.abspath(__file__))  # 获取脚本所在目录
os.chdir(script_dir)  # 将当前工作目录更改为脚本所在目录

# 获取当前目录下的所有图像文件，包括tga
# 分别匹配 .png, .jpg, .jpeg, .tga
patterns = ['*.png', '*.jpg', '*.jpeg', '*.tga']
image_files = []
for pattern in patterns:
    image_files.extend(glob.glob(os.path.join(script_dir, pattern)))
# 按修改日期排序
image_files.sort(key=os.path.getmtime, reverse=True)

# 显示文件列表
for i, file in enumerate(image_files):
    print(f"{i + 1}. {file}")

# 选择文件
print("当前工作目录:", os.getcwd())
file_index = int(input("请选择一个图像文件（数字）: ")) - 1
filename = image_files[file_index]

# 询问转换类型
conversion_type = input("请选择转换类型（1-一般图像，2-头像，3-国旗，默认为2）: ") or "2"

if conversion_type == "1":
    # 检查是否为TGA，如果是则跳转到国旗处理
    if filename.endswith('.tga'):
        base_name = filename.rsplit('.', 1)[0]
        custom_name = base_name.split('/')[-1]  # 获取不含路径的文件名
        save_flag_versions(filename, custom_name)
    else:
        # 处理非TGA图像
        pass  # 这里可以添加处理其他格式图像为一般图像的代码
elif conversion_type == "2":
    # 头像处理，包括询问国家TAG
    tag = input("请输入国家的三字母TAG（必填，自动转为全大写）: ").upper()
    assert len(tag) == 3, "TAG必须是三个字母"
    dir_name = f"leaders/{tag}"
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    with Image(filename=filename) as img:
        img.compression = 'dxt5'
        img.resize(156, 210)
        output_filename = os.path.join(dir_name, get_custom_filename(filename.rsplit('.', 1)[0], '.dds', False))
        img.save(filename=output_filename)
        print(f"图像已保存为: {output_filename}")
elif conversion_type == "3":
    # 国旗处理，直接使用TGA文件的逻辑
    base_name = filename.rsplit('.', 1)[0]
    custom_name = input("请输入生成国旗文件的名字（回车保持原名，空格将转为下划线）: ").strip().replace(' ', '_') or base_name.split('/')[-1]
    save_flag_versions(filename, custom_name)
else:
    print("无效的选项。")
