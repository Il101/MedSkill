# Инструкция по установке MedSkill

> Это инструкция для оригинальных скиллов (`skills/medical/`). Есть
> доработанный форк с более безопасной обработкой inbox и RAG-сверкой
> референсов/критериев — см. `med-plugin/README.md`.

> **Не медицинская консультация.** Скиллы не заменяют врача — они помогают
> организовать твои же документы и предположить, на что стоит обратить
> внимание. Решения о диагнозе и лечении принимает только врач.

## Требования

1. **Claude Code** - CLI инструмент от Anthropic
   - Установка: следуйте инструкциям на [официальном сайте](https://docs.anthropic.com/claude/docs/claude-code)
   - Убедитесь, что у вас есть API ключ

2. **Obsidian** (для медицинских скиллов)
   - Скачайте с [официального сайта](https://obsidian.md/)
   - Создайте волт для медицинских записей

3. **Git** (опционально, для клонирования репозитория)

## Установка

### Шаг 1: Клонирование репозитория

#### macOS / Linux

```bash
cd ~/Documents/GitHub
git clone <URL_вашего_репозитория> MedSkill
cd MedSkill
```

#### Windows (PowerShell)

```powershell
cd $env:USERPROFILE\Documents\GitHub
git clone <URL_вашего_репозитория> MedSkill
cd MedSkill
```

#### Windows (Command Prompt)

```cmd
cd %USERPROFILE%\Documents\GitHub
git clone <URL_вашего_репозитория> MedSkill
cd MedSkill
```

Или скачайте и распакуйте архив вручную.

### Шаг 2: Установка скиллов

Выберите один из двух способов:

#### Способ 1: Символические ссылки (рекомендуется)

Символические ссылки позволяют редактировать скиллы в репозитории, и изменения сразу будут доступны в Claude Code.

##### macOS / Linux

```bash
cd ~/.claude/skills/

# Медицинские скиллы
ln -s ~/Documents/GitHub/MedSkill/skills/medical/med-init
ln -s ~/Documents/GitHub/MedSkill/skills/medical/med-history
ln -s ~/Documents/GitHub/MedSkill/skills/medical/med-index
ln -s ~/Documents/GitHub/MedSkill/skills/medical/med-merge-history
ln -s ~/Documents/GitHub/MedSkill/skills/medical/med-metrics
ln -s ~/Documents/GitHub/MedSkill/skills/medical/med-process-inbox
```

**Проверка:**
```bash
ls -la ~/.claude/skills/ | grep med-
```

##### Windows (PowerShell от имени администратора)

```powershell
cd $env:USERPROFILE\.claude\skills

# Медицинские скиллы
New-Item -ItemType SymbolicLink -Path "med-init" -Target "$env:USERPROFILE\Documents\GitHub\MedSkill\skills\medical\med-init"
New-Item -ItemType SymbolicLink -Path "med-history" -Target "$env:USERPROFILE\Documents\GitHub\MedSkill\skills\medical\med-history"
New-Item -ItemType SymbolicLink -Path "med-index" -Target "$env:USERPROFILE\Documents\GitHub\MedSkill\skills\medical\med-index"
New-Item -ItemType SymbolicLink -Path "med-merge-history" -Target "$env:USERPROFILE\Documents\GitHub\MedSkill\skills\medical\med-merge-history"
New-Item -ItemType SymbolicLink -Path "med-metrics" -Target "$env:USERPROFILE\Documents\GitHub\MedSkill\skills\medical\med-metrics"
New-Item -ItemType SymbolicLink -Path "med-process-inbox" -Target "$env:USERPROFILE\Documents\GitHub\MedSkill\skills\medical\med-process-inbox"
```

**Примечание:** Для создания символических ссылок в Windows требуются права администратора.

**Проверка:**
```powershell
Get-ChildItem $env:USERPROFILE\.claude\skills\ | Where-Object {$_.Name -like "med-*"}
```

Вы должны увидеть ссылки на скиллы.

#### Способ 2: Копирование

Если вам не нужна синхронизация с репозиторием:

##### macOS / Linux

```bash
cp -r ~/Documents/GitHub/MedSkill/skills/medical/* ~/.claude/skills/
```

**Проверка:**
```bash
ls ~/.claude/skills/ | grep med-
```

##### Windows (PowerShell)

```powershell
Copy-Item -Path "$env:USERPROFILE\Documents\GitHub\MedSkill\skills\medical\*" -Destination "$env:USERPROFILE\.claude\skills\" -Recurse
```

**Проверка:**
```powershell
Get-ChildItem $env:USERPROFILE\.claude\skills\ | Where-Object {$_.Name -like "med-*"}
```

##### Windows (Command Prompt)

```cmd
xcopy /E /I %USERPROFILE%\Documents\GitHub\MedSkill\skills\medical %USERPROFILE%\.claude\skills\
```

**Проверка:**
```cmd
dir %USERPROFILE%\.claude\skills\ | findstr med-
```

### Шаг 3: Проверка установки

Запустите Claude Code и проверьте доступность скиллов:

```bash
claude
```

В интерфейсе Claude введите:
```
/help
```

Вы должны увидеть список установленных скиллов, включая:
- med-init
- med-history
- med-index
- med-merge-history
- med-metrics
- med-process-inbox

## Настройка медицинского волта Obsidian

**РЕКОМЕНДУЕТСЯ:** Используйте команду `/med-init` для автоматического создания структуры волта (см. раздел "Первое использование" ниже).

**Или создайте структуру вручную:**

### Шаг 1: Создание волта

1. Откройте Obsidian
2. Создайте новый волт (например, "Medical Records")
3. Выберите папку для волта

### Шаг 2: Создание структуры папок

#### macOS / Linux

```bash
cd /path/to/your/obsidian/vault

# Создайте основные папки
mkdir -p inbox
mkdir -p Документы/{Анализы,Консультации,Исследования,Выписки}
mkdir -p Направления
mkdir -p Истории
mkdir -p Показатели
```

#### Windows (PowerShell)

```powershell
cd C:\path\to\your\obsidian\vault

# Создайте основные папки
New-Item -ItemType Directory -Path "inbox" -Force
New-Item -ItemType Directory -Path "Документы\Анализы" -Force
New-Item -ItemType Directory -Path "Документы\Консультации" -Force
New-Item -ItemType Directory -Path "Документы\Исследования" -Force
New-Item -ItemType Directory -Path "Документы\Выписки" -Force
New-Item -ItemType Directory -Path "Направления" -Force
New-Item -ItemType Directory -Path "Истории" -Force
New-Item -ItemType Directory -Path "Показатели" -Force
```

#### Windows (Command Prompt)

```cmd
cd C:\path\to\your\obsidian\vault

mkdir inbox
mkdir Документы\Анализы
mkdir Документы\Консультации
mkdir Документы\Исследования
mkdir Документы\Выписки
mkdir Направления
mkdir Истории
mkdir Показатели
```

### Шаг 3: Создание файлов направлений

Создайте файлы для медицинских направлений в папке `Направления/`:

#### macOS / Linux

```bash
cd Направления

# Создайте базовые файлы
touch Терапия.md
touch Гастроэнтерология.md
touch Неврология.md
touch Кардиология.md
touch Эндокринология.md
# Добавьте другие направления по необходимости
```

#### Windows (PowerShell)

```powershell
cd Направления

# Создайте базовые файлы
New-Item -ItemType File -Path "Терапия.md" -Force
New-Item -ItemType File -Path "Гастроэнтерология.md" -Force
New-Item -ItemType File -Path "Неврология.md" -Force
New-Item -ItemType File -Path "Кардиология.md" -Force
New-Item -ItemType File -Path "Эндокринология.md" -Force
# Добавьте другие направления по необходимости
```

#### Windows (Command Prompt)

```cmd
cd Направления

rem Создайте базовые файлы
type nul > "Терапия.md"
type nul > "Гастроэнтерология.md"
type nul > "Неврология.md"
type nul > "Кардиология.md"
type nul > "Эндокринология.md"
rem Добавьте другие направления по необходимости
```

Базовый шаблон для файла направления:

```markdown
# Гастроэнтерология

## Хронология

### 2025

#### Консультации

#### Анализы

#### Исследования

#### Выписки
```

### Шаг 4: Настройка Claude Code для работы с вашим волтом

При запуске медицинских скиллов убедитесь, что вы находитесь в директории вашего Obsidian волта:

```bash
cd /path/to/your/obsidian/vault
claude
```

Или используйте команду `cd` внутри Claude Code.

## Первое использование

### Инициализация волта (рекомендуется)

Для автоматического создания структуры волта:

#### macOS / Linux

1. Создайте пустую директорию для волта:
   ```bash
   mkdir ~/Medical-Vault
   cd ~/Medical-Vault
   ```

2. Запустите Claude Code:
   ```bash
   claude
   ```

3. Выполните команду инициализации:
   ```
   /med-init
   ```

#### Windows (PowerShell)

1. Создайте пустую директорию для волта:
   ```powershell
   New-Item -ItemType Directory -Path "$env:USERPROFILE\Medical-Vault"
   cd $env:USERPROFILE\Medical-Vault
   ```

2. Запустите Claude Code:
   ```powershell
   claude
   ```

3. Выполните команду инициализации:
   ```
   /med-init
   ```

#### Windows (Command Prompt)

1. Создайте пустую директорию для волта:
   ```cmd
   mkdir %USERPROFILE%\Medical-Vault
   cd %USERPROFILE%\Medical-Vault
   ```

2. Запустите Claude Code:
   ```cmd
   claude
   ```

3. Выполните команду инициализации:
   ```
   /med-init
   ```

Это создаст полную структуру папок, файлы направлений, README с инструкциями и опционально .gitignore.

### Обработка первого медицинского документа

1. Поместите PDF или изображение медицинского документа в папку `inbox/`
2. В Claude Code:
   ```
   /med-process-inbox
   ```
3. Скилл автоматически обработает документ и создаст структурированный файл

### Создание первой истории болезни

После того как у вас есть несколько документов:

```
/med-history Гастроэнтерология
```

Скилл проанализирует все документы по этому направлению и создаст отчет.

## Обновление скиллов

### Если использовали символические ссылки

Просто обновите репозиторий:

```bash
cd ~/Documents/GitHub/MedSkill
git pull
```

Изменения будут доступны сразу.

### Если использовали копирование

Повторите процесс копирования:

```bash
cp -r ~/Documents/GitHub/MedSkill/skills/medical/* ~/.claude/skills/
```

## Удаление скиллов

Если нужно удалить скиллы:

```bash
cd ~/.claude/skills/

# Удаление медицинских скиллов
rm -rf med-init med-history med-index med-merge-history med-metrics med-process-inbox
```

## Troubleshooting

### Скилл не найден

**Проблема:** Claude Code не видит установленные скиллы

**Решение:**
1. Проверьте, что скиллы находятся в `~/.claude/skills/`
2. Убедитесь, что файлы `skill.md` или `SKILL.md` существуют
3. Перезапустите Claude Code

### Ошибка чтения PDF

**Проблема:** Скилл не может прочитать PDF файл

**Решение:**
1. Убедитесь, что файл не поврежден
2. Попробуйте конвертировать PDF в изображение (JPG/PNG)
3. Проверьте права доступа к файлу

### Файлы не создаются в Obsidian волте

**Проблема:** Скилл выполняется, но файлы не появляются

**Решение:**
1. Убедитесь, что вы находитесь в директории Obsidian волта
2. Проверьте права доступа к папкам
3. Проверьте путь к волту: `pwd` в Claude Code

### Дубликаты документов

**Проблема:** Скилл создает дубликаты документов

**Решение:**
1. Скилл `/med-process-inbox` автоматически проверяет дубликаты
2. Если дубликат все же создан, удалите его вручную
3. Запустите `/med-index` для обновления индексов

## Дополнительная помощь

Если у вас возникли проблемы:

1. Проверьте документацию Claude Code
2. Откройте issue в репозитории GitHub
3. Изучите файлы `skill.md` в папках скиллов для детальной информации

## Полезные ссылки

- [Claude Code Documentation](https://docs.anthropic.com/claude/docs/claude-code)
- [Obsidian Help](https://help.obsidian.md/)
