# Быстрый старт

## Установка за 5 минут

<details>
<summary><b>macOS / Linux</b></summary>

### 1. Клонируйте репозиторий
```bash
cd ~/Documents/GitHub
git clone <URL> MedSkill
```

### 2. Установите скиллы
```bash
cd ~/.claude/skills/
ln -s ~/Documents/GitHub/MedSkill/skills/medical/* .
```

### 3. Создайте и инициализируйте медицинский волт
```bash
mkdir ~/Medical-Vault
cd ~/Medical-Vault
claude
```

В Claude Code:
```
/med-init
```

### 4. Готово! Начните использовать
```bash
cd ~/Medical-Vault
claude
```

</details>

<details>
<summary><b>Windows (PowerShell)</b></summary>

### 1. Клонируйте репозиторий
```powershell
cd $env:USERPROFILE\Documents\GitHub
git clone <URL> MedSkill
```

### 2. Установите скиллы (от имени администратора)
```powershell
cd $env:USERPROFILE\.claude\skills
Get-ChildItem "$env:USERPROFILE\Documents\GitHub\MedSkill\skills\medical" | ForEach-Object {
    New-Item -ItemType SymbolicLink -Path $_.Name -Target $_.FullName
}
```

### 3. Создайте и инициализируйте медицинский волт
```powershell
New-Item -ItemType Directory -Path "$env:USERPROFILE\Medical-Vault"
cd $env:USERPROFILE\Medical-Vault
claude
```

В Claude Code:
```
/med-init
```

### 4. Готово! Начните использовать
```powershell
cd $env:USERPROFILE\Medical-Vault
claude
```

</details>

<details>
<summary><b>Windows (Command Prompt)</b></summary>

### 1. Клонируйте репозиторий
```cmd
cd %USERPROFILE%\Documents\GitHub
git clone <URL> MedSkill
```

### 2. Установите скиллы (копирование)
```cmd
xcopy /E /I %USERPROFILE%\Documents\GitHub\MedSkill\skills\medical %USERPROFILE%\.claude\skills\
```

### 3. Создайте и инициализируйте медицинский волт
```cmd
mkdir %USERPROFILE%\Medical-Vault
cd %USERPROFILE%\Medical-Vault
claude
```

В Claude Code:
```
/med-init
```

### 4. Готово! Начните использовать
```cmd
cd %USERPROFILE%\Medical-Vault
claude
```

</details>

## Первые шаги

### Инициализация волта (если еще не сделано)

```
/med-init
```

### Обработка медицинского документа

1. Поместите PDF/JPG документ в `inbox/`
2. В Claude Code:
```
/med-process-inbox
```

### Создание истории болезни

```
/med-history Гастроэнтерология
```

### Просмотр динамики показателей

```
/med-metrics
```

### Сводный анализ

```
/med-merge-history
```

## Структура команд

### Медицинские скиллы
- `/med-init` - инициализация волта
- `/med-process-inbox` - обработка документов из inbox
- `/med-history <Направление>` - история болезни
- `/med-index` - индексация всех документов
- `/med-merge-history` - сводная история
- `/med-metrics [показатель]` - динамика показателей

## Примеры использования

### Обработка результатов анализов

<details>
<summary><b>macOS / Linux</b></summary>

```bash
# Поместите PDF с анализами в inbox
cp ~/Downloads/blood-test.pdf ~/Medical-Vault/inbox/

# Запустите обработку
cd ~/Medical-Vault
claude
> /med-process-inbox

# Посмотрите динамику показателя
> /med-metrics Глюкоза
```

</details>

<details>
<summary><b>Windows (PowerShell)</b></summary>

```powershell
# Поместите PDF с анализами в inbox
Copy-Item "$env:USERPROFILE\Downloads\blood-test.pdf" "$env:USERPROFILE\Medical-Vault\inbox\"

# Запустите обработку
cd $env:USERPROFILE\Medical-Vault
claude
> /med-process-inbox

# Посмотрите динамику показателя
> /med-metrics Глюкоза
```

</details>

<details>
<summary><b>Windows (Command Prompt)</b></summary>

```cmd
rem Поместите PDF с анализами в inbox
copy %USERPROFILE%\Downloads\blood-test.pdf %USERPROFILE%\Medical-Vault\inbox\

rem Запустите обработку
cd %USERPROFILE%\Medical-Vault
claude
> /med-process-inbox

rem Посмотрите динамику показателя
> /med-metrics Глюкоза
```

</details>

### Подготовка к консультации врача

<details>
<summary><b>macOS / Linux</b></summary>

```bash
cd ~/Medical-Vault
claude
> /med-history Гастроэнтерология
> /med-merge-history
```

</details>

<details>
<summary><b>Windows</b></summary>

```powershell
cd $env:USERPROFILE\Medical-Vault
claude
> /med-history Гастроэнтерология
> /med-merge-history
```

</details>

Получите структурированную историю болезни с рекомендациями и вопросами для врача.

## Типичные workflow

### Ежемесячный медосмотр
1. Получили результаты анализов → сохраните PDF в `inbox/`
2. `/med-process-inbox` → документ обработан, показатели извлечены
3. `/med-metrics --abnormal` → проверка отклонений
4. `/med-history <направление>` → обновление истории

### Подготовка к приему специалиста
1. `/med-history <направление>` → история по направлению
2. `/med-merge-history` → сводная история
3. Откройте файлы в Obsidian
4. Используйте раздел "Вопросы для врача"

## Советы

- Обрабатывайте документы сразу после получения
- Создавайте истории болезни перед визитом к врачу
- Используйте `/med-metrics --abnormal` для мониторинга здоровья
- Сводная история (`/med-merge-history`) может выявить неочевидные связи

## Дальнейшее чтение

- [README.md](README.md) - полное описание скиллов
- [INSTALL.md](INSTALL.md) - детальная инструкция по установке
- Файлы `skill.md` в папках скиллов - полная документация по каждому скиллу

## Помощь

Если что-то не работает:
1. Проверьте, что вы в правильной директории (`pwd`)
2. Убедитесь, что структура папок создана
3. Прочитайте раздел Troubleshooting в [INSTALL.md](INSTALL.md)
