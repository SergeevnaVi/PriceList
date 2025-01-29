import os
import csv


class PriceMachine():
    
    def __init__(self):
        self.data = []  # Список для хранения данных о товарах
        self.result = ''  # Строка для хранения результата (по умолчанию пустая)
    
    def load_prices(self, file_path=''):
        """
        Сканирует указанный каталог и ищет файлы с прайс-листами.
        Для каждого найденного файла с названием, содержащим слово 'price',
        извлекаются данные о товаре, цене и весе.

        В файле ищутся столбцы с названиями товара, цены и веса.
        - Допустимые столбцы для товара: 'название', 'продукт', 'товар', 'наименование'.
        - Допустимые столбцы для цены: 'цена', 'розница'.
        - Допустимые столбцы для веса: 'вес', 'масса', 'фасовка'.

        Аргументы:
            file_path (str): Путь к каталогу с прайс-листами. По умолчанию - текущая директория.
        """
        files = [file_name for file_name in os.listdir() if 'price' in file_name and file_name.endswith('.csv')]

        if not files:
            print('Не найдены файлы с прайс-листами')
            return

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

                    # Поиск столбцов с нужными заголовками
                    for header in reader_file.fieldnames:
                        if any(product in header.lower() for product in product_headers):
                            product_col = header
                        elif any(price in header.lower() for price in price_headers):
                            price_col = header
                        elif any(weight in header.lower() for weight in weight_headers):
                            weight_col = header

                    if not product_col or not price_col or not weight_col:
                        print(f'В файле {file_name} отсутствуют нужные столбцы.')
                        continue

                    # Обработка строк с товаром
                    for row in reader_file:
                        try:
                            product = row[product_col].strip()
                            price = int(row[price_col].replace(',', '.'))
                            weight = int(row[weight_col].replace(',', '.'))

                            if product and price > 0 and weight > 0:
                                price_kg = round(price / weight, 1)

                                self.data.append({
                                    'product': product,
                                    'price': price,
                                    'weight': weight,
                                    'file_name': file_name,
                                    'price_kg': price_kg,
                                })
                        except ValueError:
                            print(f'Ошибка обработки строки в файле {file_name}: {row}')
            except Exception as e:
                print(f'Ошибка при обработке файла {file_name}: {e}')

    def export_to_html(self, fname='output.html'):
        """
        Экспортирует данные о товарах в HTML формат в виде таблицы.

        Создается HTML-файл с таблицей, где отображаются: номер,
        наименование товара, цена, вес, файл, цена за килограмм.

        Аргументы:
            fname (str): Имя файла для сохранения данных. По умолчанию 'output.html'.
        """
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

        for index, item in enumerate(self.data, 1):
            result += f'''
                <tr>
                    <td>{index}</td>
                    <td>{item['product']}</td>
                    <td>{item['price']}</td>
                    <td>{item['weight']}</td>
                    <td>{item['file_name']}</td>
                    <td>{item['price_kg']}</td>
                </tr>
            '''

        result += '''
            </table>
        </body>
        </html>
        '''

        with open(fname, 'w', encoding='utf-8') as file:
            file.write(result)

    def print_table(self, data):
        """
        Выводит таблицу данных о товарах в консоль.

        Аргументы:
            data (list): Список товаров для вывода.
        """
        print(f"{'№':<5} {'Наименование':<30} {'Цена':<10} {'Вес':<5} {'Файл':<15} {'Цена за кг.':<15}")
        for index, item in enumerate(data, 1):
            print(
                f"{index:<5} {item['product']:<30} {item['price']:<10} {item['weight']:<5} {item['file_name']:<15} {item['price_kg']:<15}")

    def find_text(self, text):
        """
        Ищет товары по части названия и сортирует их по цене за килограмм.

        Результаты поиска выводятся в консоль и экспортируются в HTML-файл.

        Аргументы:
            text (str): Фрагмент текста для поиска в названии товара.
        """
        text = text.lower()

        # Фильтрация товаров по фрагменту в названии
        filtered_data = [item for item in self.data if text in item.get('product', '').lower()]

        if not filtered_data:
            print("Ничего не найдено")
            return

        try:
            # Сортировка найденных товаров по цене за килограмм
            sorted_data = sorted(filtered_data, key=lambda x: x['price_kg'])

            self.print_table(sorted_data)
            self.export_to_html(fname='output.html')
        except Exception as e:
            print("Ошибка при сортировке:", e)


if __name__ == '__main__':
    pm = PriceMachine()
    pm.load_prices()

    while True:
        query = input('Введите часть названия товара для поиска (или "exit" для выхода): ')
        if query.lower() == 'exit':
            print('Работа завершена!')
            break
        pm.find_text(query)
