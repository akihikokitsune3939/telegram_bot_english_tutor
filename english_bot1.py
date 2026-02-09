import random
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# База данных задач с вариантами ответов (50 задач по английскому)
ENGLISH_TASKS = [
    {
        'id': 1,
        'type': 'grammar',
        'question': 'Choose the correct option: I ___ to the cinema yesterday.',
        'options': ['go', 'went', 'have gone', 'am going'],
        'correct_answer': 1,
        'explanation': 'В этом предложении нужно использовать Past Simple для действия, которое произошло вчера.'
    },
    {
        'id': 2,
        'type': 'vocabulary',
        'question': 'What is the synonym for "happy"?',
        'options': ['sad', 'joyful', 'angry', 'tired'],
        'correct_answer': 1,
        'explanation': 'Синонимы к слову "happy": joyful, cheerful, glad, delighted.'
    },
    {
        'id': 3,
        'type': 'grammar',
        'question': 'Fill in the blank: She ___ playing the piano for 5 years.',
        'options': ['has been', 'is', 'was', 'were'],
        'correct_answer': 0,
        'explanation': 'Present Perfect Continuous используется для действия, которое началось в прошлом и продолжается до настоящего.'
    },
    {
        'id': 4,
        'type': 'vocabulary',
        'question': 'What does "benevolent" mean?',
        'options': ['selfish', 'kind and generous', 'angry', 'intelligent'],
        'correct_answer': 1,
        'explanation': 'Benevolent (доброжелательный) - showing kindness and goodwill.'
    },
    {
        'id': 5,
        'type': 'grammar',
        'question': 'Choose the correct sentence:',
        'options': ['They is students.', 'They are students.', 'They am students.', 'They be students.'],
        'correct_answer': 1,
        'explanation': 'С местоимением "they" используется глагол "are".'
    },
    {
        'id': 6,
        'type': 'vocabulary',
        'question': 'Which word is an antonym for "expand"?',
        'options': ['increase', 'contract', 'grow', 'extend'],
        'correct_answer': 1,
        'explanation': 'Expand (расширять) - Contract (сокращать) - антонимы.'
    },
    {
        'id': 7,
        'type': 'grammar',
        'question': 'Correct the mistake: "She don\'t like apples."',
        'options': ['She doesn\'t likes apples.', 'She doesn\'t like apples.', 'She don\'t likes apples.', 'She not like apples.'],
        'correct_answer': 1,
        'explanation': 'В 3-м лице единственного числа используется "doesn\'t" + инфинитив без to.'
    },
    {
        'id': 8,
        'type': 'vocabulary',
        'question': 'What is the meaning of "to procrastinate"?',
        'options': ['To do things quickly', 'To delay or postpone tasks', 'To organize efficiently', 'To finish early'],
        'correct_answer': 1,
        'explanation': 'Procrastinate - откладывать на потом, медлить.'
    },
    {
        'id': 9,
        'type': 'reading',
        'question': 'Read: "John loves reading books. He visits the library every week." How often does John visit the library?',
        'options': ['Every day', 'Every week', 'Every month', 'Every year'],
        'correct_answer': 1,
        'explanation': 'В тексте сказано "every week" - каждую неделю.'
    },
    {
        'id': 10,
        'type': 'grammar',
        'question': 'Which is the correct comparative form: "This book is ___ than that one."',
        'options': ['interestinger', 'more interesting', 'interestinger', 'most interesting'],
        'correct_answer': 1,
        'explanation': 'Для многосложных прилагательных используется "more + прилагательное".'
    },
    {
        'id': 11,
        'type': 'vocabulary',
        'question': 'Choose the correct phrasal verb: "Please ___ the light when you leave."',
        'options': ['turn off', 'turn up', 'turn over', 'turn on'],
        'correct_answer': 0,
        'explanation': 'Turn off - выключать; turn up - увеличивать громкость; turn over - переворачивать; turn on - включать.'
    },
    {
        'id': 12,
        'type': 'grammar',
        'question': 'Complete with the correct preposition: "I\'m good ___ math."',
        'options': ['at', 'in', 'on', 'with'],
        'correct_answer': 0,
        'explanation': 'Используется конструкция "to be good at something" - быть хорошим в чем-то.'
    },
    {
        'id': 13,
        'type': 'vocabulary',
        'question': 'What is a "synonym"?',
        'options': ['A word with opposite meaning', 'A word with similar meaning', 'A homophone', 'A palindrome'],
        'correct_answer': 1,
        'explanation': 'Синонимы - слова с похожим значением.'
    },
    {
        'id': 14,
        'type': 'grammar',
        'question': 'Choose the correct question form: "___ you speak English?"',
        'options': ['Do', 'Does', 'Are', 'Is'],
        'correct_answer': 0,
        'explanation': 'Для местоимения "you" используется вспомогательный глагол "do".'
    },
    {
        'id': 15,
        'type': 'listening',
        'question': 'Imagine you hear: "I\'d like to book a table for two." Where is this conversation taking place?',
        'options': ['At a library', 'At a restaurant', 'At a hotel', 'At a cinema'],
        'correct_answer': 1,
        'explanation': '"Book a table" - заказать столик (в ресторане).'
    },
    {
        'id': 16,
        'type': 'vocabulary',
        'question': 'Which word means "a person who teaches"?',
        'options': ['student', 'teacher', 'learner', 'professor'],
        'correct_answer': 1,
        'explanation': 'Teacher - учитель, преподаватель.'
    },
    {
        'id': 17,
        'type': 'grammar',
        'question': 'Put the words in correct order: "never / I / have / to / been / London"',
        'options': ['I never have been to London.', 'I have never been to London.', 'Never I have been to London.', 'I have been never to London.'],
        'correct_answer': 1,
        'explanation': 'Наречие "never" ставится между вспомогательным глаголом "have" и основным глаголом "been".'
    },
    {
        'id': 18,
        'type': 'vocabulary',
        'question': 'What is the opposite of "ancient"?',
        'options': ['old', 'modern', 'historic', 'classical'],
        'correct_answer': 1,
        'explanation': 'Ancient (древний) - Modern (современный) - антонимы.'
    },
    {
        'id': 19,
        'type': 'grammar',
        'question': 'Choose the correct form: "If I ___ you, I would study harder."',
        'options': ['am', 'was', 'were', 'be'],
        'correct_answer': 2,
        'explanation': 'Во втором типе условных предложений используется "were" для всех лиц.'
    },
    {
        'id': 20,
        'type': 'vocabulary',
        'question': 'What does "ambiguous" mean?',
        'options': ['clear', 'unclear or having multiple meanings', 'obvious', 'simple'],
        'correct_answer': 1,
        'explanation': 'Ambiguous - двусмысленный, имеющий несколько значений.'
    },
    # Новые задачи (21-50)
    {
        'id': 21,
        'type': 'grammar',
        'question': 'Choose the correct form: "By next year, I ___ English for 5 years."',
        'options': ['will study', 'will have studied', 'will be studying', 'study'],
        'correct_answer': 1,
        'explanation': 'Future Perfect используется для действий, которые завершатся к определенному моменту в будущем.'
    },
    {
        'id': 22,
        'type': 'vocabulary',
        'question': 'What does "ephemeral" mean?',
        'options': ['permanent', 'lasting a very short time', 'beautiful', 'expensive'],
        'correct_answer': 1,
        'explanation': 'Ephemeral - мимолетный, недолговечный.'
    },
    {
        'id': 23,
        'type': 'grammar',
        'question': 'Choose the correct article: "She is ___ university student."',
        'options': ['a', 'an', 'the', 'no article'],
        'correct_answer': 0,
        'explanation': 'Перед словом "university", которое начинается с согласного звука, используется "a".'
    },
    {
        'id': 24,
        'type': 'vocabulary',
        'question': 'What is a "metaphor"?',
        'options': ['Direct comparison using "like" or "as"', 'Implied comparison without "like" or "as"', 'Repeating consonant sounds', 'Exaggeration for effect'],
        'correct_answer': 1,
        'explanation': 'Метафора - это скрытое сравнение без использования "like" или "as".'
    },
    {
        'id': 25,
        'type': 'grammar',
        'question': 'Choose the correct passive form: "The letter ___ yesterday."',
        'options': ['was written', 'wrote', 'has written', 'is written'],
        'correct_answer': 0,
        'explanation': 'Passive voice в Past Simple: was/were + past participle.'
    },
    {
        'id': 26,
        'type': 'vocabulary',
        'question': 'What does "ubiquitous" mean?',
        'options': ['rare', 'found everywhere', 'invisible', 'unique'],
        'correct_answer': 1,
        'explanation': 'Ubiquitous - вездесущий, встречающийся повсюду.'
    },
    {
        'id': 27,
        'type': 'grammar',
        'question': 'Choose the correct modal verb: "You ___ smoke here. It\'s prohibited."',
        'options': ['can', 'must', 'mustn\'t', 'should'],
        'correct_answer': 2,
        'explanation': 'Mustn\'t выражает запрет.'
    },
    {
        'id': 28,
        'type': 'vocabulary',
        'question': 'What is the meaning of "serendipity"?',
        'options': ['Planned discovery', 'Accidental discovery of something good', 'Scientific research', 'Hard work'],
        'correct_answer': 1,
        'explanation': 'Serendipity - счастливая случайность, неожиданная удача.'
    },
    {
        'id': 29,
        'type': 'reading',
        'question': 'Read: "The weather was terrible. It was raining cats and dogs." What does "raining cats and dogs" mean?',
        'options': ['Animals were falling from the sky', 'Raining very heavily', 'Raining lightly', 'Not raining at all'],
        'correct_answer': 1,
        'explanation': 'Idiom "raining cats and dogs" означает "льет как из ведра".'
    },
    {
        'id': 30,
        'type': 'grammar',
        'question': 'Choose the correct conditional: "If I had known, I ___ you."',
        'options': ['would help', 'would have helped', 'helped', 'will help'],
        'correct_answer': 1,
        'explanation': 'Third Conditional: if + past perfect, would have + past participle.'
    },
    {
        'id': 31,
        'type': 'vocabulary',
        'question': 'What does "quintessential" mean?',
        'options': ['ordinary', 'representing the most perfect example', 'strange', 'unimportant'],
        'correct_answer': 1,
        'explanation': 'Quintessential - квинтэссенция, самый типичный пример.'
    },
    {
        'id': 32,
        'type': 'grammar',
        'question': 'Choose the correct word order: "___ to the party last night?"',
        'options': ['Did you go', 'Went you', 'You went', 'You did go'],
        'correct_answer': 0,
        'explanation': 'В вопросах в Past Simple используется did + subject + infinitive.'
    },
    {
        'id': 33,
        'type': 'vocabulary',
        'question': 'What is a "paradox"?',
        'options': ['A simple statement', 'A self-contradictory statement that may be true', 'A scientific fact', 'A question'],
        'correct_answer': 1,
        'explanation': 'Парадокс - утверждение, которое противоречит само себе, но может быть верным.'
    },
    {
        'id': 34,
        'type': 'grammar',
        'question': 'Choose the correct relative pronoun: "This is the book ___ I bought yesterday."',
        'options': ['who', 'which', 'where', 'when'],
        'correct_answer': 1,
        'explanation': '"Which" используется для предметов, "who" - для людей.'
    },
    {
        'id': 35,
        'type': 'vocabulary',
        'question': 'What does "meticulous" mean?',
        'options': ['careless', 'very careful and precise', 'quick', 'average'],
        'correct_answer': 1,
        'explanation': 'Meticulous - педантичный, очень внимательный к деталям.'
    },
    {
        'id': 36,
        'type': 'grammar',
        'question': 'Choose the correct tense: "Look! It ___."',
        'options': ['snows', 'is snowing', 'snowed', 'has snowed'],
        'correct_answer': 1,
        'explanation': 'Present Continuous используется для действий, происходящих в момент речи.'
    },
    {
        'id': 37,
        'type': 'vocabulary',
        'question': 'What is the meaning of "eloquent"?',
        'options': ['silent', 'able to express ideas clearly and effectively', 'angry', 'confused'],
        'correct_answer': 1,
        'explanation': 'Eloquent - красноречивый, хорошо выражающий мысли.'
    },
    {
        'id': 38,
        'type': 'grammar',
        'question': 'Choose the correct preposition: "I\'m looking forward ___ seeing you."',
        'options': ['to', 'for', 'at', 'with'],
        'correct_answer': 0,
        'explanation': 'Выражение "look forward to" требует предлога "to" + gerund.'
    },
    {
        'id': 39,
        'type': 'vocabulary',
        'question': 'What does "resilient" mean?',
        'options': ['fragile', 'able to recover quickly from difficulties', 'permanent', 'weak'],
        'correct_answer': 1,
        'explanation': 'Resilient - устойчивый, способный быстро восстанавливаться.'
    },
    {
        'id': 40,
        'type': 'grammar',
        'question': 'Choose the correct form: "Three years ___ a long time to wait."',
        'options': ['is', 'are', 'were', 'have'],
        'correct_answer': 0,
        'explanation': 'Периоды времени обычно рассматриваются как единое целое и требуют глагола в единственном числе.'
    },
    {
        'id': 41,
        'type': 'vocabulary',
        'question': 'What is an "oxymoron"?',
        'options': ['Simple phrase', 'Combination of contradictory words', 'Long sentence', 'Question without answer'],
        'correct_answer': 1,
        'explanation': 'Оксюморон - сочетание противоречащих друг другу слов.'
    },
    {
        'id': 42,
        'type': 'grammar',
        'question': 'Choose the correct comparative: "This test is ___ than the last one."',
        'options': ['difficulter', 'more difficult', 'difficulter', 'most difficult'],
        'correct_answer': 1,
        'explanation': 'Для многосложных прилагательных используется "more + adjective".'
    },
    {
        'id': 43,
        'type': 'vocabulary',
        'question': 'What does "alleviate" mean?',
        'options': ['make worse', 'make less severe', 'ignore', 'complicate'],
        'correct_answer': 1,
        'explanation': 'Alleviate - облегчать, смягчать.'
    },
    {
        'id': 44,
        'type': 'grammar',
        'question': 'Choose the correct tag question: "She can swim, ___?"',
        'options': ['can she', 'can\'t she', 'does she', 'is she'],
        'correct_answer': 1,
        'explanation': 'В tag questions используется противоположная форма вспомогательного глагола.'
    },
    {
        'id': 45,
        'type': 'vocabulary',
        'question': 'What is the meaning of "diligent"?',
        'options': ['lazy', 'hard-working and careful', 'careless', 'slow'],
        'correct_answer': 1,
        'explanation': 'Diligent - прилежный, усердный.'
    },
    {
        'id': 46,
        'type': 'grammar',
        'question': 'Choose the correct form: "I wish I ___ taller."',
        'options': ['am', 'was', 'were', 'will be'],
        'correct_answer': 2,
        'explanation': 'После "wish" используется were для всех лиц в нереальных ситуациях.'
    },
    {
        'id': 47,
        'type': 'vocabulary',
        'question': 'What does "verbose" mean?',
        'options': ['concise', 'using too many words', 'silent', 'clear'],
        'correct_answer': 1,
        'explanation': 'Verbose - многословный, излишне подробный.'
    },
    {
        'id': 48,
        'type': 'grammar',
        'question': 'Choose the correct sentence:',
        'options': ['The team are winning.', 'The team is winning.', 'The team were winning.', 'The team am winning.'],
        'correct_answer': 1,
        'explanation': '"Team" как единое целое требует глагола в единственном числе.'
    },
    {
        'id': 49,
        'type': 'vocabulary',
        'question': 'What is "sarcasm"?',
        'options': ['Literal meaning', 'Saying the opposite of what you mean to mock', 'Compliment', 'Question'],
        'correct_answer': 1,
        'explanation': 'Сарказм - использование слов, означающих противоположное, для насмешки.'
    },
    {
        'id': 50,
        'type': 'grammar',
        'question': 'Choose the correct form: "By the time we arrived, the movie ___."',
        'options': ['started', 'had started', 'was starting', 'starts'],
        'correct_answer': 1,
        'explanation': 'Past Perfect используется для действия, которое завершилось до другого действия в прошлом.'
    }
]

# Статистика пользователей
user_stats = {}

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_stats:
        user_stats[user_id] = {'correct': 0, 'total': 0, 'current_task': None}
    
    welcome_text = """
    🎓 *English Learning Bot*
    
    📚 *Теперь доступно 50 интерактивных задач!*
    
    Доступные команды:
    /start - Начать работу
    /task - Получить случайную задачу по английскому
    /stats - Ваша статистика
    /topics - Показать темы задач
    
    Выбирайте ответы с помощью кнопок под задачей.
    Каждая задача имеет подробное объяснение!
    """
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

# Команда /topics
async def show_topics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topics_text = """
    📖 *Темы задач в боте:*
    
    • *Грамматика (Grammar)* - 20 задач
      - Времена глаголов
      - Условные предложения
      - Пассивный залог
      - Модальные глаголы
      - Предлоги
      - Артикли
    
    • *Словарный запас (Vocabulary)* - 20 задач
      - Синонимы и антонимы
      - Значения сложных слов
      - Фразовые глаголы
      - Идиомы
    
    • *Чтение (Reading)* - 5 задач
      - Понимание текста
      - Идиомы в контексте
    
    • *Аудирование (Listening)* - 5 задач
      - Понимание ситуаций
      - Контекст разговора
    
    Всего: 50 задач разных уровней сложности!
    
    Начните обучение: /task
    """
    await update.message.reply_text(topics_text, parse_mode='Markdown')

# Команда /task
async def get_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # Инициализация статистики, если пользователь новый
    if user_id not in user_stats:
        user_stats[user_id] = {'correct': 0, 'total': 0, 'current_task': None}
    
    # Выбираем случайную задачу
    task = random.choice(ENGLISH_TASKS)
    
    # Сохраняем выбранную задачу в статистике пользователя
    user_stats[user_id]['current_task'] = task
    
    # Создаем кнопки с вариантами ответов
    keyboard = []
    for i, option in enumerate(task['options']):
        # Используем callback_data в формате: answer_<user_id>_<task_id>_<option_index>
        callback_data = f"answer_{user_id}_{task['id']}_{i}"
        keyboard.append([InlineKeyboardButton(f"{chr(65+i)}) {option}", callback_data=callback_data)])
    
    # Добавляем кнопку для пропуска
    keyboard.append([
        InlineKeyboardButton("⏭ Пропустить", callback_data=f"skip_{user_id}"),
        InlineKeyboardButton("ℹ️ Подсказка", callback_data=f"hint_{user_id}")
    ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Формируем текст задачи
    task_text = f"""
    📚 *Задача #{task['id']} из 50* | Тип: {task['type']}
    ⭐ Сложность: {get_difficulty(task['id'])}
    
    *{task['question']}*
    
    Выберите правильный вариант ответа:
    """
    
    # Если это сообщение с командой, отправляем новое сообщение
    if update.message:
        await update.message.reply_text(task_text, parse_mode='Markdown', reply_markup=reply_markup)
    # Если это callback query (например, после пропуска)
    elif update.callback_query:
        await update.callback_query.edit_message_text(
            text=task_text,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )

# Функция определения сложности задачи
def get_difficulty(task_id):
    if task_id <= 10:
        return "🟢 Начальный"
    elif task_id <= 30:
        return "🟡 Средний"
    elif task_id <= 40:
        return "🟠 Продвинутый"
    else:
        return "🔴 Эксперт"

# Обработчик нажатия на кнопки с ответами
async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Важно: подтверждаем callback query
    
    # Разбираем callback_data
    data = query.data
    parts = data.split('_')
    
    if parts[0] == 'skip':
        user_id = int(parts[1])
        # Показываем ответ на пропущенную задачу
        if user_id in user_stats and user_stats[user_id]['current_task']:
            task = user_stats[user_id]['current_task']
            correct_answer = task['options'][task['correct_answer']]
            explanation = task['explanation']
            
            result_text = f"""
            ⏭ *Задача #{task['id']} пропущена*
            
            *Правильный ответ:* {correct_answer}
            
            *Объяснение:* {explanation}
            
            *Сложность:* {get_difficulty(task['id'])}
            
            Получить новую задачу: /task
            Или посмотреть статистику: /stats
            """
            
            # Обновляем статистику
            user_stats[user_id]['total'] += 1
            user_stats[user_id]['current_task'] = None
            
            # Создаем кнопки для продолжения
            keyboard = [
                [InlineKeyboardButton("🔄 Новая задача", callback_data="new_task")],
                [InlineKeyboardButton("📊 Статистика", callback_data="show_stats")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                text=result_text,
                parse_mode='Markdown',
                reply_markup=reply_markup
            )
        return
    
    elif parts[0] == 'hint':
        user_id = int(parts[1])
        if user_id in user_stats and user_stats[user_id]['current_task']:
            task = user_stats[user_id]['current_task']
            hint_text = get_hint_for_task(task)
            await query.answer(hint_text, show_alert=True)
        return
    
    if parts[0] == 'answer':
        user_id = int(parts[1])
        task_id = int(parts[2])
        selected_option = int(parts[3])
        
        # Ищем задачу в базе данных
        task = None
        for t in ENGLISH_TASKS:
            if t['id'] == task_id:
                task = t
                break
        
        if not task:
            await query.edit_message_text("Задача не найдена. Попробуйте снова: /task")
            return
        
        # Проверяем ответ
        is_correct = (selected_option == task['correct_answer'])
        correct_answer = task['options'][task['correct_answer']]
        selected_answer = task['options'][selected_option]
        explanation = task['explanation']
        
        # Обновляем статистику пользователя
        if user_id not in user_stats:
            user_stats[user_id] = {'correct': 0, 'total': 0, 'current_task': None}
        
        user_stats[user_id]['total'] += 1
        if is_correct:
            user_stats[user_id]['correct'] += 1
        
        # Формируем ответ
        if is_correct:
            result_icon = "✅"
            result_text = "ПРАВИЛЬНО! Отличная работа!"
        else:
            result_icon = "❌"
            result_text = "НЕПРАВИЛЬНО! Попробуйте еще раз!"
        
        # Создаем новый набор кнопок для продолжения
        keyboard = [
            [InlineKeyboardButton("🔄 Новая задача", callback_data="new_task")],
            [
                InlineKeyboardButton("📊 Статистика", callback_data="show_stats"),
                InlineKeyboardButton("📖 Темы", callback_data="show_topics_callback")
            ]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        response_text = f"""
        {result_icon} *{result_text}*
        
        *Задача #{task['id']}* | Сложность: {get_difficulty(task['id'])}
        
        *Ваш ответ:* {selected_answer}
        *Правильный ответ:* {correct_answer}
        
        *Объяснение:* {explanation}
        
        *Ваша статистика:* {user_stats[user_id]['correct']}/{user_stats[user_id]['total']} правильных ответов
        *Успешность:* {calculate_success_rate(user_id):.1f}%
        
        Выберите действие:
        """
        
        # Сохраняем ID пользователя в контексте для кнопок продолжения
        context.user_data['last_user_id'] = user_id
        
        await query.edit_message_text(
            text=response_text,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    
    elif query.data == "new_task":
        user_id = context.user_data.get('last_user_id', update.effective_user.id)
        if user_id in user_stats:
            user_stats[user_id]['current_task'] = None
        
        # Отправляем новую задачу
        await get_task(update, context)
    
    elif query.data == "show_stats":
        await show_stats_callback(update, context)
    
    elif query.data == "show_topics_callback":
        await show_topics_callback(update, context)

# Функция для подсказок
def get_hint_for_task(task):
    hints_by_type = {
        'grammar': [
            "Обратите внимание на время глагола",
            "Проверьте согласование подлежащего и сказуемого",
            "Вспомните правила использования артиклей",
            "Подумайте о порядке слов в предложении"
        ],
        'vocabulary': [
            "Попробуйте вспомнить контекст использования этого слова",
            "Подумайте о корне слова и возможных родственных словах",
            "Вспомните синонимы или антонимы",
            "Попробуйте перевести слово дословно"
        ],
        'reading': [
            "Ищите ответ прямо в тексте",
            "Обратите внимание на ключевые слова",
            "Подумайте о контексте всего предложения",
            "Не забывайте про логику повествования"
        ],
        'listening': [
            "Представьте себе ситуацию",
            "Какие слова являются ключевыми?",
            "Где обычно происходит такой разговор?",
            "О чем могут говорить люди в такой ситуации?"
        ]
    }
    
    hints = hints_by_type.get(task['type'], ["Внимательно прочитайте вопрос и варианты ответов"])
    return random.choice(hints)

# Функция расчета процента успеха
def calculate_success_rate(user_id):
    if user_id in user_stats and user_stats[user_id]['total'] > 0:
        return (user_stats[user_id]['correct'] / user_stats[user_id]['total']) * 100
    return 0

# Команда /stats
async def show_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id not in user_stats or user_stats[user_id]['total'] == 0:
        await update.message.reply_text("📊 У вас еще нет статистики. Решите несколько задач: /task")
        return
    
    stats = user_stats[user_id]
    total = stats['total']
    correct = stats['correct']
    success_rate = calculate_success_rate(user_id)
    
    # Определяем уровень
    level = get_user_level(success_rate)
    
    # Рассчитываем прогресс
    progress = min(total, 50)  # Максимум 50 задач
    
    # Создаем прогресс-бар
    progress_bar = create_progress_bar(progress, 50)
    
    stats_text = f"""
    📊 *Ваша статистика:*
    
    *Решено задач:* {correct} из {total}
    *Успешность:* {success_rate:.1f}%
    *Уровень:* {level['name']} {level['emoji']}
    
    *Прогресс по всем задачам:*
    {progress_bar} {progress}/50
    
    *Рекомендации:* {level['recommendation']}
    
    Продолжить обучение: /task
    """
    
    await update.message.reply_text(stats_text, parse_mode='Markdown')

# Callback для статистики
async def show_stats_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = context.user_data.get('last_user_id', update.effective_user.id)
    
    if user_id not in user_stats or user_stats[user_id]['total'] == 0:
        await query.edit_message_text("📊 У вас еще нет статистики. Решите несколько задач!")
        return
    
    stats = user_stats[user_id]
    total = stats['total']
    correct = stats['correct']
    success_rate = calculate_success_rate(user_id)
    level = get_user_level(success_rate)
    progress = min(total, 50)
    progress_bar = create_progress_bar(progress, 50)
    
    # Создаем кнопки для возврата
    keyboard = [
        [InlineKeyboardButton("🔄 Новая задача", callback_data="new_task")],
        [InlineKeyboardButton("📖 Темы", callback_data="show_topics_callback")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    stats_text = f"""
    📊 *Ваша статистика:*
    
    *Решено задач:* {correct} из {total}
    *Успешность:* {success_rate:.1f}%
    *Уровень:* {level['name']} {level['emoji']}
    
    *Прогресс:* {progress_bar} {progress}/50
    
    *Рекомендация:* {level['recommendation']}
    
    Для продолжения нажмите кнопку ниже:
    """
    
    await query.edit_message_text(
        text=stats_text,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

# Callback для тем
async def show_topics_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("🔄 Новая задача", callback_data="new_task")],
        [InlineKeyboardButton("📊 Статистика", callback_data="show_stats")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    topics_text = """
    📖 *Темы задач:*
    
    • *Грамматика* - 20 задач
    • *Словарный запас* - 20 задач
    • *Чтение* - 5 задач
    • *Аудирование* - 5 задач
    
    Всего: 50 задач разных уровней сложности!
    
    Начните обучение:
    """
    
    await query.edit_message_text(
        text=topics_text,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

# Функция определения уровня пользователя
def get_user_level(success_rate):
    if success_rate >= 90:
        return {
            'name': 'Эксперт',
            'emoji': '🎖',
            'recommendation': 'Отлично! Продолжайте в том же духе!'
        }
    elif success_rate >= 75:
        return {
            'name': 'Продвинутый',
            'emoji': '🏅',
            'recommendation': 'Хорошие результаты! Учите больше сложных слов.'
        }
    elif success_rate >= 60:
        return {
            'name': 'Средний',
            'emoji': '🥉',
            'recommendation': 'Неплохо! Практикуйте грамматику больше.'
        }
    elif success_rate >= 40:
        return {
            'name': 'Начинающий',
            'emoji': '📚',
            'recommendation': 'Продолжайте заниматься! Решайте больше задач.'
        }
    else:
        return {
            'name': 'Новичок',
            'emoji': '🌱',
            'recommendation': 'Начните с более простых задач и повторяйте материал.'
        }

# Функция создания прогресс-бара
def create_progress_bar(current, total, length=10):
    filled = int((current / total) * length)
    empty = length - filled
    return '█' * filled + '░' * empty

# Обработчик ошибок
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.error(f"Exception while handling an update: {context.error}")
    if update.callback_query:
        await update.callback_query.message.reply_text("⚠️ Произошла ошибка. Пожалуйста, попробуйте еще раз.")
    elif update.message:
        await update.message.reply_text("⚠️ Произошла ошибка. Пожалуйста, попробуйте еще раз.")


# тут токен бота
TOKEN = "YOUR_TOKEN_BOT"

# Создаем приложение
application = Application.builder().token(TOKEN).build()

# Регистрируем обработчики команд
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("task", get_task))
application.add_handler(CommandHandler("stats", show_stats))
application.add_handler(CommandHandler("topics", show_topics))

# Регистрируем обработчики callback query (нажатия на кнопки)
application.add_handler(CallbackQueryHandler(handle_answer, pattern="^(answer_|skip_|hint_|new_task|show_stats|show_topics_callback)"))

# Регистрируем обработчик ошибок
application.add_error_handler(error_handler)

# Запускаем бота
print("Бот запущен...")
print(f"Всего задач в базе: {len(ENGLISH_TASKS)}")
application.run_polling(allowed_updates=Update.ALL_TYPES)
