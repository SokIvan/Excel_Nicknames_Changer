from libs import requests
from libs import subprocess

def check_for_updates():
    REPO_OWNER = 'SokIvan'  # Ваш логин на GitHub
    REPO_NAME = 'Excel_Nicknames_Changer'  # Название Вашего репозитория
    with open('../Files/Version', 'r') as f:
        read = f.read()
        current_version = read.split("\n")[0].split(":")[-1]
        print(current_version)
        response = requests.get(f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/latest')
        if response.status_code == 200:
            latest_version = response.json()['tag_name']
            if latest_version != current_version:
                print('Доступна новая версия')
                url = response.json()['assets'][0]['browser_download_url']
                if download_update(url):
                    install_update()
            else:
                print('У вас актуальная версия')


def download_update(url):
    response = requests.get(url)
    if response.status_code == 200:
        with open('update.zip', 'wb') as f:
            f.write(response.content)
        print('Обновление успешно скачано')
        return True
    else:
        print('Ошибка при скачивании обновления')
        return False

def install_update():
    subprocess.run(['unzip', 'update.zip'])
    subprocess.run(['rm', 'update.zip'])
    print('Обновление успешно установлено')