from functions.get_files_info import get_files_info

print(get_files_info("calculator", ".") + "\n")

print(get_files_info("calculator", "pkg") + "\n")

print(get_files_info("calculator", "/bin") + "\n")

print(get_files_info("calculator", "../") + "\n")