import os
import json
import csv


class PriceMachine():
    
    def __init__(self):
        self.data = []
        self.result = ''
        self.name_length = 0
    
    def load_prices(self, file_path=''):
        '''
            Сканирует указанный каталог. Ищет файлы со словом price в названии.
            В файле ищет столбцы с названием товара, ценой и весом.
            Допустимые названия для столбца с товаром:
                товар
                название
                наименование
                продукт
                
            Допустимые названия для столбца с ценой:
                розница
                цена
                
            Допустимые названия для столбца с весом (в кг.)
                вес
                масса
                фасовка
        '''
        files = [file_name for file_name in os.listdir() if 'price' in file_name and file_name.endswith('.csv')]

        for file_name in files:
            try:
                with open(file_name, 'r', encoding='utf-8') as f:
                    reader_file = csv.DictReader(f)

                    product_headers = ['название', 'продукт', 'товар', 'наименование']
                    price_headers = ['цена', 'розница']
                    weight_headers = ['вес', 'масса', 'фасовка']

                    product_col = None
                    price_col = None
                    weight_col = None

                    for header in reader_file.fieldnames:
                        if any(product in header.lower() for product in product_headers):
                            product_col = header
                        elif any(price in header.lower() for price in price_headers):
                            price_col = header
                        elif any(weight in header.lower() for weight in weight_headers):
                            weight_col = header

                    for row in reader_file:
                        pass

                    if product_col and price_col and weight_col:
                        break

                if not product_col or not price_col or not weight_col:
                    print(f'В файле {file_name} отсутствуют нужные столбцы.')
                    continue

            except Exception as e:
                print(f'Ошибка при обработке файла {file_name}: {e}')


    def export_to_html(self, fname='output.html'):
        result = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Позиции продуктов</title>
        </head>
        <body>
            <table>
                <tr>
                    <th>Номер</th>
                    <th>Название</th>
                    <th>Цена</th>
                    <th>Фасовка</th>
                    <th>Файл</th>
                    <th>Цена за кг.</th>
                </tr>
        '''
    
    def find_text(self, text):
        pass

    
pm = PriceMachine()
print(pm.load_prices())

'''
    Логика работы программы
'''
print('the end')
print(pm.export_to_html())
