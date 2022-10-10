import requests
import lxml.html
import json

# получаем главную страницу
response = requests.get('https://stihi.ru/poems/list.html')
tree = lxml.html.fromstring(response.text)
# получаем каждую категорию
for category in tree.xpath('//ul/ul/li/a'):
    # получаем страницу категории
    response = requests.get('https://stihi.ru' + category.get('href'))
    tree = lxml.html.fromstring(response.text)
    print(response)
    # выводим ссылку категории и название
    print(category.get('href'), category.text)

    # получаем каждую страницу
    for page in tree.xpath('//index/div[@class="textlink nounline"]/a'):
        # выводим текст номера страницы и ссылку на нее
        print(page.text_content(), page.get('href'))

        # получаем страницу с названиями стихов
        response = requests.get('https://stihi.ru' + page.get('href'))
        tree = lxml.html.fromstring(response.text)
        # получаем название всех стихов на странице
        for stih_name in tree.xpath('//index/ul/li/a'):
            # выводим название стиха и ссылку на него
            print(stih_name.text, stih_name.get('href'))

            # получаем страницу каждого стиха
            response = requests.get('https://stihi.ru' + stih_name.get('href'))
            tree = lxml.html.fromstring(response.text)
            # выводим информацию о стихе: название, автора, весь текст, дату

            author = tree.xpath('//index/div/em/a')
            if len(author):
                author = author[0].text
            print(author)

            stih_text = tree.xpath('//index/div[@class="text"]')
            if len(stih_text):
                stih_text = stih_text[0].text_content()
            print(stih_text)
            result = {'category_name': category.text, 'name': stih_name.text, 'author': author, 'text': stih_text}

            with open("stihi.txt", "a") as file:
                file.write(f'{json.dumps(result, ensure_ascii=False)}\n')
