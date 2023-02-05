import urllib.request

img_url = "https://files.yande.re/sample/b864bc0702364eae6ef970ea7dbe8e4d/yande.re%201061771%20sample%20amiya_%28arknights%29%20animal_ears%20arknights%20bunny_ears%20suyama_kara.jpg"

urllib.request.urlretrieve(img_url, "./images/teste.png")
