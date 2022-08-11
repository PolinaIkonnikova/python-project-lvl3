## Utility Page Loader
Save any static page and use it offline!
### Hexlet tests and linter status:
[![Actions Status](https://github.com/PolinaIkonnikova/python-project-lvl3/workflows/hexlet-check/badge.svg)](https://github.com/PolinaIkonnikova/python-project-lvl3/actions)
[![PyCI](https://github.com/PolinaIkonnikova/python-project-lvl3/actions/workflows/PyCI.yml/badge.svg)](https://github.com/PolinaIkonnikova/python-project-lvl3/actions/workflows/PyCI.yml)
[![Test Coverage](https://api.codeclimate.com/v1/badges/9247ba55b8f1dbb38bc8/test_coverage)](https://codeclimate.com/github/PolinaIkonnikova/python-project-lvl3/test_coverage)
[![Maintainability](https://api.codeclimate.com/v1/badges/9247ba55b8f1dbb38bc8/maintainability)](https://codeclimate.com/github/PolinaIkonnikova/python-project-lvl3/maintainability)

### Сoобщение наставнику:
- Хотелось бы изменить запись логов - info отправлять в файл, особенно все, что связано с ресурсами, а не в strout, в log_configs закомментирована часть настроек, уберу или добавлю после проверки.
- Не всегда определяется код запроса к странице, бывает, что сразу вылетает ошибка соединения, поэтому в модуле два раза перехвачиваю connection error, не знаю, как лучше сделать. 

#### for install: 
```
make package-install
```
#### for reference information
```
page-loader -h
```
You need to enter a url and a path for downloading 
(the default path is the working directory):

Example 1 (100% загрузка в директорию по умолчанию, ошибка при повторном скачивании):
[![asciicast](https://asciinema.org/a/uI5RSueTx7JtB1h3mwqHNPxjX.svg)](https://asciinema.org/a/uI5RSueTx7JtB1h3mwqHNPxjX)

Example 2 (Загрузка в указанную директорию, страница без ресурсов, ошибка неверной директории):
[![asciicast](https://asciinema.org/a/XLcIhbsPZSYLI1OKPEXsGZZHg.svg)](https://asciinema.org/a/XLcIhbsPZSYLI1OKPEXsGZZHg)

Example 3 (Неполная загрузка ресурсов, логи успешных и неудачных загрузок ресурсов):
[![asciicast](https://asciinema.org/a/IQVlzRYqFvsHqpJblhG0mkUvj.svg)](https://asciinema.org/a/IQVlzRYqFvsHqpJblhG0mkUvj)
