import os

def get_files_info(working_directory, directory="."):
    try:
        #print("Working dir:", working_directory)
        #print("Directory:", directory)
        working_dir_abs = os.path.abspath(working_directory)
        #print("Working dir abs:", working_dir_abs)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        #print("Target dir:", target_dir)
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir])
        #print("Valid target dir:", valid_target_dir)
        if valid_target_dir != working_dir_abs:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        files = []
        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir, item)
            size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            files.append(f"- {item}: file_size={size} bytes, is_dir={is_dir}")
        return "\n".join(files)
    except Exception as e:
        return f"Error: {e}"
