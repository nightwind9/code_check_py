import argparse
import os
import subprocess
from git import Repo

def get_changed_files(repo_path):
    """
    获取最新一次提交中变更的文件列表

    参数:
    repo_path (str): Git仓库的本地路径

    返回:
    changed_files (list): 变更的文件列表
    """
    repo = Repo(repo_path)

    # 获取最新一次提交
    head_commit = repo.head.commit

    # 获取最新一次提交与其父提交之间的差异
    diff = head_commit.diff(head_commit.parents[0])  # 假设父提交总是存在的

    changed_files = []
    for file_diff in diff:
        # 只关注变更类型为'AM'（添加和修改）和'D'（删除）的文件
        if file_diff.change_type in ['A', 'M', 'D']:
            # 获取变更的文件路径
            file_path = os.path.join(repo_path, file_diff.a_path)
            changed_files.append(file_path)

    return changed_files

def get_all_python_files(directory):
    """
    获取目录下所有的Python文件

    参数:
    directory (str): 目标目录的路径

    返回:
    python_files (list): Python文件的列表
    """
    python_files = []

    # 遍历目录及其子目录
    for root, dirs, files in os.walk(directory):
        for file in files:
            # 检查文件扩展名是否为'.py'
            if file.endswith(".py"):
                # 获取Python文件的绝对路径
                python_file_path = os.path.join(root, file)
                python_files.append(python_file_path)

    return python_files
'''
def find_conf_files(directory):
    """
    在指定目录中查找以.conf结尾的文件

    参数:
    directory (str): 目标目录的路径

    返回:
    conf_files (list): 符合条件的文件列表
    """
    conf_files = []

    # 获取目录中的所有文件和子目录
    files_and_dirs = os.listdir(directory)
    for item in files_and_dirs:
        item_path = os.path.join(directory, item)

        # 判断是否为文件且以.conf结尾
        if os.path.isfile(item_path) and item.endswith(".conf"):
            conf_files.append(item_path)

    return conf_files
'''
def find_conf_files(directory):
    """
    在指定目录及其子目录中查找所有的.conf文件,以及上两级目录中符合条件的文件

    参数:
    directory (str): 目标目录的路径

    返回:
    conf_files (list): 符合条件的文件列表
    """
    conf_files = []

    # 遍历当前目录及其子目录中的文件
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".conf"):
                conf_files.append(os.path.join(root, file))

    # 遍历上级目录及上两级目录中的文件
    parent_directory = os.path.dirname(directory)
    for _ in range(2):  # 上两级目录
        if parent_directory != directory:
            for file in os.listdir(parent_directory):
                if file.endswith(".conf"):
                    conf_files.append(os.path.join(parent_directory, file))
        parent_directory = os.path.dirname(parent_directory)

    return conf_files

def run_pylint(rcfile, source_files, output_file):
    """
    运行Pylint命令并指定参数

    参数:
    rcfile (str): Pylint配置文件路径
    source_files (list): 要检查的源文件列表
    output_file (str): 输出文件路径

    返回:
    result (str): Pylint命令输出结果
    """
    
    #plugins (str): 要加载的Pylint插件
    #output_format (str): 输出格式（jsonextended等）
    plugins = "pylint_json2html"
    output_format= "jsonextended"

    # 构造Pylint命令
    pylint_cmd = f"pylint --rcfile={rcfile} --load-plugins={plugins} --output-format={output_format} {' '.join(source_files)} > {output_file}"

    subprocess.run(pylint_cmd, shell=True)
    

def pylint_json2html(input_file, output_file):
    """
    将Pylint的JSON输出转换为HTML格式

    参数:
    input_file (str): 输入JSON文件路径
    output_file (str): 输出HTML文件路径
    """
    # 构造转换命令
    json2html_cmd = f"pylint-json2html -f jsonextended -o {output_file} {input_file}"

    # 运行转换命令
    subprocess.run(json2html_cmd, shell=True)

if __name__ == "__main__":
    # 创建ArgumentParser对象
    parser = argparse.ArgumentParser(description="在命令行中指定函数处理路径")

    # 添加路径选项
    parser.add_argument("path", help="要处理的路径")

    # 添加检查变更或全部文件选项
    parser.add_argument("-f", "--function", dest="function", default="all", choices=["all", "chg"], help="要调用的函数")

    # 解析命令行参数
    args = parser.parse_args()

    # 根据选项调用相应函数处理
    if args.function == "all":
        check_files = get_all_python_files(args.path)
        files_type = "All file(s) in the directory"
    elif args.function == "chg":
        check_files = get_changed_files(args.path)
        files_type = "Changed file(s) in the directory"
    else:
        print("无效的函数选项：", args.function)

    #打印需要检查的所有文件路径
    print(f'{files_type} is(are) as follows: ')
    for file_path in check_files:
        print(file_path)

    #将路径list转换为string类型
    rcfile_path = "".join(find_conf_files(args.path))

    #设置文件名并生成报告
    output_json_file = "report.json"
    output_html_file = "report.html"
    run_pylint(rcfile_path, check_files, output_json_file)
    pylint_json2html(output_json_file, output_html_file)
