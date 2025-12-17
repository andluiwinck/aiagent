import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file = os.path.commonpath([working_dir_abs, target_file])
        if valid_target_file != working_dir_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_file.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        absolute_file_path = os.path.abspath(target_file)
        command = ["python", absolute_file_path]
        if args:
            command.extend(args)
        result = subprocess.run(command, capture_output=True, text=True, timeout=30, cwd=working_dir_abs)
        output_parts = []
        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")
        if not result.stdout and not result.stderr:
            output_parts.append("No output produced")
        else:
            if result.stdout:
                output_parts.append(f"STDOUT: {result.stdout}")
            if result.stderr:
                output_parts.append(f"STDERR: {result.stderr}")
        return "\n".join(output_parts)
    except Exception as e:
        return f"Error: executing Python file: {e}"