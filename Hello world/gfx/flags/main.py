import os
import glob
from wand.image import Image
script_dir = os.path.dirname(os.path.abspath(__file__))  # 获取脚本所在目录
os.chdir(script_dir)  # 将当前工作目录更改为脚本所在目录
def get_custom_filename(default_name, extension, replace_space=True):
    custom_name = input("请输入生成文件的名字（回车保持不变）: ").strip()
    if replace_space:
        custom_name = custom_name.replace(' ', '_')
    if custom_name:
        return custom_name + extension
    else:
        return default_name + extension

# 获取当前目录下的所有图像文件
image_files = glob.glob('./*.[pj][np]g')  # 匹配 .png, .jpg, .jpeg
# 按修改日期排序
image_files.sort(key=os.path.getmtime, reverse=True)

# 显示文件列表
for i, file in enumerate(image_files):
    print(f"{i + 1}. {file}")

# 选择文件
file_index = int(input("请选择一个图像文件（数字）: ")) - 1
filename = image_files[file_index]

# 询问转换类型
conversion_type = input("请选择转换类型（1-一般图像，2-头像，3-国旗，默认为2）: ") or "2"

if conversion_type == "1" or conversion_type == "2":
    # 转换为DDS格式
    with Image(filename=filename) as img:
        img.compression = 'dxt5'
        if conversion_type == "2":
            # 调整为头像分辨率
            img.resize(156, 210)
        output_filename = get_custom_filename(filename.rsplit('.', 1)[0], '.dds', False)
        img.save(filename=output_filename)
        print(f"图像已保存为: {output_filename}")
elif conversion_type == "3":
    # 转换为TGA格式，不同分辨率
    resolutions = [(82, 52), (41, 26), (10, 7)]
    directories = ["flags", "flags/medium", "flags/small"]
    base_name = filename.rsplit('.', 1)[0]
    custom_name = input("请输入生成国旗文件的名字（回车保持原名，空格将转为下划线）: ").strip().replace(' ', '_') or base_name
    for res, dir_name in zip(resolutions, directories):
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        with Image(filename=filename) as img:
            img.resize(*res)
            img.flip()  # 上下翻转图像
            new_filename = os.path.join(dir_name, custom_name + '.tga')
            img.save(filename=new_filename)
            print(f"图像已保存为: {new_filename}")
else:
    print("无效的选项。")
