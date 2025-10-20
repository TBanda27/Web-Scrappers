from bs4 import BeautifulSoup
import requests


html = requests.get('https://www.nike.com/ie/?cp=72331783026_search_-nike%20ireland-g-22719762149-190067986708-e-c-EN-extended-760472669973-aud-1896772579106:kwd-416265637906-9192439&gclsrc=aw.ds&ds_rl=1252249&gad_source=1&gad_campaignid=22719762149&gbraid=0AAAAADq9vlNqDDlaGZwEqOIiXFdXNbTVz&gclid=CjwKCAjwu9fHBhAWEiwAzGRC_1rayVyhKSO5W70LOrm5uSnn0Z9fghM8btNzqKuZzUxTvslN8bpO_RoCjsAQAvD_BwE')
page = BeautifulSoup(html.content, 'lxml')

print(page.prettify())