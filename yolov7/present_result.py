import os

result_dir = 'results'
files = os.listdir(result_dir)
print("Generated files:")
for file in files:
    print(file)
