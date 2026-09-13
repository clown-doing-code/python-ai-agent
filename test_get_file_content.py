from functions.get_file_content import get_file_content

result = get_file_content("calculator", "lorem.txt")
print(f"lorem.txt length: {len(result)}")
print(f"lorem.txt truncated: {'truncated' in result}")

result = get_file_content("calculator", "main.py")
print("Result for 'main.py' directory:")
print(result)

result = get_file_content("calculator", "pkg/calculator.py")
print("Result for 'pkg' directory:")
print(result)

result = get_file_content("calculator", "/bin/cat")
print("Result for '/bin/cat' directory:")
print(result)

result = get_file_content("calculator", "pkg/does_not_exist.py")
print("Result for 'pkg/does_not_exist.py' directory:")
print(result)
