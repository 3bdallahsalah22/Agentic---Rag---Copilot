from pathlib import Path 

#creating working directory 

root = Path(".")

#folders to creare 

folders = [
    "app/api",
    "app/core",
    "app/rag",
    "app/services",
    "data",
    "templates" , 
    "statics",
    "uploads",
    "tests"
]

#files to create

files = [
    "app/main.py",
    "ingest_sample_kb.py"
    "run.py",
    ".env"
]

#create folders
for folder in folders :
    (root/folder).mkdir(parents=True , exist_ok=True)


#create files
for file in files :
    (root/file).touch(exist_ok=True)
    
    
    
    
    
    
print("project structure created succssefully.")