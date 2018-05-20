import os
import requests
import zipfile

NIKTO_SRC_DIRNAME = "nikto_src"  # папка хранения исходников тулзы
NIKTO_MOD_PATH = os.path.join("adapters", "nikto")  # строение проекта
FULL_PATH_NIKTO_SRC_DIR = os.path.join(NIKTO_MOD_PATH, NIKTO_SRC_DIRNAME)
PATH_NIKTO_PRJ = os.path.join("nikto-master", "program", "nikto.pl")  # строение тулзы

NIKTO_SRC_URL = "https://github.com/sullo/nikto/archive/master.zip"  # берем с гитхаба

try:
    os.mkdir(FULL_PATH_NIKTO_SRC_DIR)
except FileExistsError:
    pass  # значит уже установлен, на выход
else:
    current_dir = os.getcwd()
    os.chdir(FULL_PATH_NIKTO_SRC_DIR)

    r = requests.get(NIKTO_SRC_URL)

    temp_file = NIKTO_SRC_URL.rpartition("/")[-1]

    with open(temp_file, "wb") as f:
        f.write(r.content)

    with zipfile.ZipFile(temp_file) as n_zip:
        n_zip.extractall()

    os.remove(temp_file)

    os.chdir(current_dir)

PATH_NIKTO_TOOL = os.path.join(os.getcwd(), NIKTO_MOD_PATH, NIKTO_SRC_DIRNAME, PATH_NIKTO_PRJ)
if not os.path.exists(PATH_NIKTO_TOOL):
    raise "Nikto setup error"

os.chmod(PATH_NIKTO_TOOL, 0o544)
