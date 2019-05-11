# Image binarisation

## About

Данный прект содержит реализацию алгоритма бинаризации изображений `Adaptive Tresholding`, описанний здесь: [link](http://people.scs.carleton.ca/~roth/iit-publications-iti/docs/gerh-50002.pdf). Реализация приведена на языке `python`, необходимые библиотеки для работы программы приведены в файле `requirements.txt`. Тестовые изображения находятся в папке `raw`, результаты бинаризации представлены в папке `binarized`.

## Requirements

* PIL
* numpy 
* pandas 
* tabulate

Для установки пакетов используется `pip`:

```
> pip instar -r requirements.txt
```

## Launching 

Для запуска, в папке проекта запускаем `script.py`:

```
> python3 script.py
```

## Time elapsing

В файле `times.md` представленны времена работы алгоритма на соответствующих изображениях (в секундах). На основании этих данных, можем сделать вывод, что алгоритм работает со скоростью порядка `8.7*10^(-6) сек/пикс`