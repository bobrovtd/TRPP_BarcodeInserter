# Инструмент для автоматизации прикрепления штрихкодов

## Описание проекта

**Инструмент для автоматизации прикрепления штрихкодов** — это кроссплатформенное desktop-приложение для упрощения процесса прикрепления штрихкодов к документам.

**Основное назначение**:  
Приложение извлекает штрихкоды из Excel-файлов, экспортированных из 1С, и автоматически прикрепляет их к выбранным документам.

### Основные функции

- **Извлечение штрихкодов**  
  Анализирует Excel-файлы и сохраняет штрихкоды во внутренней базе данных

- **Обработка документов**  
  Автоматически прикрепляет штрихкоды к выбранным документам

- **Гибкий импорт данных**  
  Поддерживает два режима загрузки:
  - Пакетная обработка всех файлов в директории
  - Выборочная загрузка отдельных файлов

- **Кроссплатформенность**  
  Работает на различных операционных системах

## Установка

### Требования

- Python 3.8 или новее

### Инструкция по установке

1. **Клонирование репозитория**:
   ```bash
   git clone https://github.com/bobrovtd/TRPP_BarcodeInserter
   cd TRPP_BarcodeInserter
   ```

2. **Установка зависимостей**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Запуск приложения**:
   ```bash
   python src/main.py
   ```

## Использование

### 1. Прикрепление штрихкодов к документам

**Как использовать**:
1. Выберите папку с документами для обработки
2. Убедитесь, что база штрихкодов заполнена
3. Укажите папку для сохранения результатов
4. Нажмите **"Старт"**

**Результат**:  
Документы с интегрированными штрихкодами в указанной директории.

### 2. Обновление базы штрихкодов

**Как использовать**:
1. Выберите режим:
   - 🗂 Обработка всей папки
   - 📄 Загрузка отдельных файлов
2. Укажите источник данных
3. Нажмите **"Старт"**

**Формат файлов**:  
Программа ожидает Excel файлы сгенерированные при помощи 1C.
```