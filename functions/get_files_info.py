import os

def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        if os.path.commonpath([working_dir_abs, target_dir]) != working_dir_abs:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        
        target_dir_contents = ""
        entries_names = os.listdir(target_dir)
        for name in entries_names:
            target_dir_contents += f"- {name}: file_size={os.path.getsize(target_dir + "/" + name)} bytes, is_dir={os.path.isdir(target_dir + "/" + name)}\n"
        return target_dir_contents.rstrip("\n")
    
    except:
        return "Error: something went wrong"