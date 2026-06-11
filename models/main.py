import requests


if __name__ == '__main__':
    
    r = requests.get('https://worldcup26.ir/get/games')
    
    print(r)