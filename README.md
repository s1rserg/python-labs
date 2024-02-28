Лабораторна робота №1 з дисципліни "Проектування алгоритмів"

Варіант 23: Збалансоване багатошляхове злиття

Інструкція для виконання:

1. клонувати репозиторій
2. перейти в командний рядок
3. перейти у папку репозиторію
4. сd src
5. cd lab1
6. python main.py # для стандартної версії
7. python mods.py # для модифікованої версії
8. вхідний файл - у папці src a.txt, вихідний - у папці src b1.txt або с1.txt

---

Лабораторна робота №2 з дисципліни "Проектування алгоритмів"

Варіант 22: 8-puzzle: LDFS, RBFS + H2

Інструкція для виконання:

1. клонувати репозиторій
2. перейти в командний рядок
3. перейти у папку репозиторію
4. сd src
5. cd lab2
6. pip install pywin32
7. python main.py

// вхідний файл -- input.txt, у нього вводити матрицю 3\*3, цифри розділені пробілами

---

Лабораторна робота №3 з дисципліни "Проектування алгоритмів"

Варіант 22: Файли з щільним індексом з областю переповнення, метод Шарра.

Реалізовано додаткове завдання візуалізації структури ключів.

Інструкція для виконання:

1. клонувати репозиторій
2. перейти в командний рядок
3. перейти у папку репозиторію
4. сd src
5. cd lab3
6. python main.py

Для вибору створеного файла, у полі select ввести назву без розширення, натиснути select.

Для нового файлу, у полі create ввести назву, натиснути create, опціонально ввести у поле generate назву та натиснути кнопку для генерації.

Дані при роботі програми зберігаються в ОП, тому для запису в файл, натиснути кнопку update.

При закритті програми хрестиком запис проводиться самостійно.

Файл з щільним індексом складається з трьох файлів *index.txt, *main.txt, \*overflow.txt, для індексного файла, головного файла та області переповнення.

---

Лабораторна робота №4 з дисципліни "Проектування алгоритмів"

Варіант 22: Задача про рюкзак (місткість P=250, 100 предметів, цінність предметів
від 2 до 30 (випадкова), вага від 1 до 25 (випадкова)), генетичний
алгоритм (початкова популяція 100 осіб кожна по 1 різному предмету,
оператор схрещування триточковий 25%, мутація з ймовірністю 5%
змінюємо тільки 1 випадковий ген). Розробити власний оператор
локального покращення.

Інструкція для виконання:

1. клонувати репозиторій
2. перейти в командний рядок
3. перейти у папку репозиторію
4. сd src
5. cd lab4
6. pip install matplotlib
7. python main.py

Для відображення графіку залежності розв'язку від числа ітерацій:

python main.py gr

Для вводу предметів з файлу(кожний рядок: weight, value), кількість рядків подільна на 4:

python main.py ngr назва файлу з розширенням (python main.py ngr input.txt) - без графіку

python main.py gr назва файлу з розширенням - з графіком

---

Лабораторна робота №5 з дисципліни "Проектування алгоритмів"

Варіант 22: Задача про найкоротший шлях + Бджолиний алгоритм

Інструкція для виконання:

1. клонувати репозиторій
2. перейти в командний рядок
3. перейти у папку репозиторію
4. сd src
5. cd lab5
6. python main.py
