import random
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# База данных задач по английскому (50 задач)
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

# База данных задач по немецкому (30 задач)
GERMAN_TASKS = [
    {
        'id': 1,
        'type': 'grammar',
        'question': 'Выберите правильный артикль: ___ Haus (дом)',
        'options': ['der', 'die', 'das', 'den'],
        'correct_answer': 2,
        'explanation': 'Слово "Haus" - среднего рода, поэтому используется артикль "das".'
    },
    {
        'id': 2,
        'type': 'vocabulary',
        'question': 'Как переводится слово "Buch"?',
        'options': ['книга', 'ручка', 'стол', 'окно'],
        'correct_answer': 0,
        'explanation': 'Buch - книга (среднего рода, das Buch).'
    },
    {
        'id': 3,
        'type': 'grammar',
        'question': 'Выберите правильную форму глагола: Ich ___ Deutsch. (Я говорю по-немецки.)',
        'options': ['spreche', 'sprecht', 'sprechen', 'sprichst'],
        'correct_answer': 0,
        'explanation': 'Глагол "sprechen" в 1 лице единственного числа: ich spreche.'
    },
    {
        'id': 4,
        'type': 'vocabulary',
        'question': 'Как будет "спасибо" по-немецки?',
        'options': ['Bitte', 'Danke', 'Entschuldigung', 'Hallo'],
        'correct_answer': 1,
        'explanation': 'Danke - спасибо; Bitte - пожалуйста; Entschuldigung - извините; Hallo - привет.'
    },
    {
        'id': 5,
        'type': 'grammar',
        'question': 'Выберите правильное местоимение: ___ bin Student. (Я студент.)',
        'options': ['Du', 'Er', 'Ich', 'Wir'],
        'correct_answer': 2,
        'explanation': 'Ich - я (1 лицо единственного числа).'
    },
    {
        'id': 6,
        'type': 'vocabulary',
        'question': 'Как переводится "der Tisch"?',
        'options': ['стул', 'стол', 'шкаф', 'кровать'],
        'correct_answer': 1,
        'explanation': 'der Tisch - стол (мужского рода).'
    },
    {
        'id': 7,
        'type': 'grammar',
        'question': 'Выберите правильный артикль: ___ Frau (женщина)',
        'options': ['der', 'die', 'das', 'den'],
        'correct_answer': 1,
        'explanation': 'Слово "Frau" - женского рода, поэтому используется артикль "die".'
    },
    {
        'id': 8,
        'type': 'vocabulary',
        'question': 'Как будет "доброе утро" по-немецки?',
        'options': ['Guten Tag', 'Guten Abend', 'Gute Nacht', 'Guten Morgen'],
        'correct_answer': 3,
        'explanation': 'Guten Morgen - доброе утро; Guten Tag - добрый день; Guten Abend - добрый вечер; Gute Nacht - спокойной ночи.'
    },
    {
        'id': 9,
        'type': 'grammar',
        'question': 'Выберите правильную форму: Wie ___ du? (Как тебя зовут?)',
        'options': ['heiße', 'heißt', 'heißen', 'heiß'],
        'correct_answer': 1,
        'explanation': 'Глагол "heißen" во 2 лице единственного числа: du heißt.'
    },
    {
        'id': 10,
        'type': 'vocabulary',
        'question': 'Как переводится слово "die Schule"?',
        'options': ['университет', 'школа', 'работа', 'больница'],
        'correct_answer': 1,
        'explanation': 'die Schule - школа (женского рода).'
    },
    {
        'id': 11,
        'type': 'grammar',
        'question': 'Выберите правильную форму глагола: Wir ___ in Berlin. (Мы живем в Берлине.)',
        'options': ['wohne', 'wohnst', 'wohnt', 'wohnen'],
        'correct_answer': 3,
        'explanation': 'Глагол "wohnen" в 1 лице множественного числа: wir wohnen.'
    },
    {
        'id': 12,
        'type': 'vocabulary',
        'question': 'Как будет "до свидания" по-немецки?',
        'options': ['Hallo', 'Tschüss', 'Ja', 'Nein'],
        'correct_answer': 1,
        'explanation': 'Tschüss - пока, до свидания (неформальное).'
    },
    {
        'id': 13,
        'type': 'grammar',
        'question': 'Выберите правильный артикль: ___ Kind (ребенок)',
        'options': ['der', 'die', 'das', 'den'],
        'correct_answer': 2,
        'explanation': 'Слово "Kind" - среднего рода, поэтому используется артикль "das".'
    },
    {
        'id': 14,
        'type': 'vocabulary',
        'question': 'Как переводится "der Stuhl"?',
        'options': ['стол', 'стул', 'диван', 'кресло'],
        'correct_answer': 1,
        'explanation': 'der Stuhl - стул (мужского рода).'
    },
    {
        'id': 15,
        'type': 'grammar',
        'question': 'Выберите правильную форму: ___ kommst aus Deutschland? (Ты из Германии?)',
        'options': ['Wo', 'Wer', 'Wie', 'Was'],
        'correct_answer': 0,
        'explanation': 'Wo - где, откуда; Wer - кто; Wie - как; Was - что.'
    },
    {
        'id': 16,
        'type': 'vocabulary',
        'question': 'Как будет "извините" по-немецки?',
        'options': ['Danke', 'Bitte', 'Entschuldigung', 'Tschüss'],
        'correct_answer': 2,
        'explanation': 'Entschuldigung - извините.'
    },
    {
        'id': 17,
        'type': 'grammar',
        'question': 'Выберите правильную форму глагола: Er ___ Fußball. (Он играет в футбол.)',
        'options': ['spiele', 'spielst', 'spielt', 'spielen'],
        'correct_answer': 2,
        'explanation': 'Глагол "spielen" в 3 лице единственного числа: er spielt.'
    },
    {
        'id': 18,
        'type': 'vocabulary',
        'question': 'Как переводится слово "das Wasser"?',
        'options': ['воздух', 'огонь', 'вода', 'земля'],
        'correct_answer': 2,
        'explanation': 'das Wasser - вода (среднего рода).'
    },
    {
        'id': 19,
        'type': 'grammar',
        'question': 'Выберите правильное числительное: eins, zwei, ___ (один, два, три)',
        'options': ['vier', 'fünf', 'drei', 'sechs'],
        'correct_answer': 2,
        'explanation': 'Немецкие числительные: 1 - eins, 2 - zwei, 3 - drei, 4 - vier, 5 - fünf, 6 - sechs.'
    },
    {
        'id': 20,
        'type': 'vocabulary',
        'question': 'Как будет "пожалуйста" по-немецки?',
        'options': ['Danke', 'Bitte', 'Ja', 'Nein'],
        'correct_answer': 1,
        'explanation': 'Bitte - пожалуйста (также используется как "не за что" в ответ на "спасибо").'
    },
    {
        'id': 21,
        'type': 'grammar',
        'question': 'Выберите правильный артикль: ___ Mann (мужчина)',
        'options': ['der', 'die', 'das', 'den'],
        'correct_answer': 0,
        'explanation': 'Слово "Mann" - мужского рода, поэтому используется артикль "der".'
    },
    {
        'id': 22,
        'type': 'vocabulary',
        'question': 'Как переводится "die Mutter"?',
        'options': ['отец', 'мать', 'сестра', 'брат'],
        'correct_answer': 1,
        'explanation': 'die Mutter - мать (женского рода).'
    },
    {
        'id': 23,
        'type': 'grammar',
        'question': 'Выберите правильную форму: Woher ___ Sie? (Откуда Вы?)',
        'options': ['kommen', 'kommst', 'kommt', 'komme'],
        'correct_answer': 0,
        'explanation': 'Глагол "kommen" в вежливой форме Sie (Вы): Sie kommen.'
    },
    {
        'id': 24,
        'type': 'vocabulary',
        'question': 'Как будет "хлеб" по-немецки?',
        'options': ['das Brot', 'der Käse', 'die Milch', 'das Fleisch'],
        'correct_answer': 0,
        'explanation': 'das Brot - хлеб; der Käse - сыр; die Milch - молоко; das Fleisch - мясо.'
    },
    {
        'id': 25,
        'type': 'grammar',
        'question': 'Выберите правильное время: Ich ___ gestern ins Kino gegangen. (Я вчера ходил в кино.)',
        'options': ['bin', 'habe', 'war', 'gehe'],
        'correct_answer': 0,
        'explanation': 'Perfekt с глаголом движения "gehen" образуется с вспомогательным глаголом "sein".'
    },
    {
        'id': 26,
        'type': 'vocabulary',
        'question': 'Как переводится "das Auto"?',
        'options': ['поезд', 'автобус', 'машина', 'самолет'],
        'correct_answer': 2,
        'explanation': 'das Auto - автомобиль, машина (среднего рода).'
    },
    {
        'id': 27,
        'type': 'grammar',
        'question': 'Выберите правильный падеж: Ich gebe ___ Buch. (Я даю книгу.)',
        'options': ['der', 'die', 'das', 'dem'],
        'correct_answer': 2,
        'explanation': 'Прямое дополнение в Akkusativ: das Buch (винительный падеж).'
    },
    {
        'id': 28,
        'type': 'vocabulary',
        'question': 'Как будет "хорошо" по-немецки?',
        'options': ['schlecht', 'gut', 'langsam', 'schnell'],
        'correct_answer': 1,
        'explanation': 'gut - хорошо; schlecht - плохо; langsam - медленно; schnell - быстро.'
    },
    {
        'id': 29,
        'type': 'grammar',
        'question': 'Выберите правильное отрицание: Ich ___ nicht müde. (Я не устал.)',
        'options': ['bin', 'bist', 'sind', 'seid'],
        'correct_answer': 0,
        'explanation': 'Глагол "sein" в 1 лице единственного числа: ich bin.'
    },
    {
        'id': 30,
        'type': 'vocabulary',
        'question': 'Как переводится "der Vater"?',
        'options': ['мать', 'отец', 'сын', 'дочь'],
        'correct_answer': 1,
        'explanation': 'der Vater - отец (мужского рода).'
    }
]

# Базы данных по языкам
LANGUAGE_DATABASES = {
    'english': {
        'name': 'Английский',
        'flag': '🇬🇧',
        'tasks': ENGLISH_TASKS,
        'count': len(ENGLISH_TASKS)
    },
    'german': {
        'name': 'Немецкий',
        'flag': '🇩🇪',
        'tasks': GERMAN_TASKS,
        'count': len(GERMAN_TASKS)
    }
}

# Статистика пользователей
user_stats = {}
# Язык по умолчанию для пользователей
user_languages = {}
# Для хранения использованных подсказок (user_id: {task_id: True})
used_hints = {}

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # Инициализация статистики, если пользователь новый
    if user_id not in user_stats:
        user_stats[user_id] = {
            'english': {'correct': 0, 'total': 0, 'used_hints': 0}, 
            'german': {'correct': 0, 'total': 0, 'used_hints': 0}, 
            'current_task': None
        }
    
    # Устанавливаем язык по умолчанию, если не выбран
    if user_id not in user_languages:
        user_languages[user_id] = 'english'
    
    current_lang = user_languages[user_id]
    lang_info = LANGUAGE_DATABASES[current_lang]
    
    welcome_text = f"""
    🎓 *Language Learning Bot*
    
    🌍 *Текущий язык:* {lang_info['flag']} {lang_info['name']}
    📚 *Доступно задач:* {lang_info['count']}
    
    Доступные команды:
    /start - Начать работу
    /task - Получить случайную задачу
    /stats - Ваша статистика
    /topics - Показать темы задач
    /language - Сменить язык обучения
    
    Выбирайте ответы с помощью кнопок под задачей.
    ℹ️ *Подсказка* - убирает 2 неправильных варианта ответа!
    
    Каждая задача имеет подробное объяснение!
    """
    
    # Создаем клавиатуру с кнопкой смены языка
    keyboard = [
        [InlineKeyboardButton("🌍 Сменить язык", callback_data="change_language")],
        [InlineKeyboardButton("📚 Получить задачу", callback_data="get_task_callback")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_text, parse_mode='Markdown', reply_markup=reply_markup)

# Команда /language
async def change_language_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_language_selection(update, context)

# Показать выбор языка
async def show_language_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = []
    
    for lang_key, lang_data in LANGUAGE_DATABASES.items():
        button_text = f"{lang_data['flag']} {lang_data['name']} ({lang_data['count']} задач)"
        keyboard.append([InlineKeyboardButton(button_text, callback_data=f"select_lang_{lang_key}")])
    
    # Кнопка возврата
    keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data="back_to_main")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = """
    🌍 *Выберите язык для изучения:*
    
    Вы можете переключаться между языками в любое время.
    Ваша статистика сохраняется отдельно для каждого языка.
    """
    
    if update.message:
        await update.message.reply_text(text, parse_mode='Markdown', reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.edit_message_text(
            text=text,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )

# Команда /task
async def get_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # Инициализация статистики, если пользователь новый
    if user_id not in user_stats:
        user_stats[user_id] = {
            'english': {'correct': 0, 'total': 0, 'used_hints': 0}, 
            'german': {'correct': 0, 'total': 0, 'used_hints': 0}, 
            'current_task': None
        }
    
    # Устанавливаем язык по умолчанию, если не выбран
    if user_id not in user_languages:
        user_languages[user_id] = 'english'
    
    current_lang = user_languages[user_id]
    lang_info = LANGUAGE_DATABASES[current_lang]
    
    # Выбираем случайную задачу
    task = random.choice(lang_info['tasks'])
    
    # Сохраняем выбранную задачу в статистике пользователя
    user_stats[user_id]['current_task'] = task
    user_stats[user_id]['current_lang'] = current_lang
    
    # Создаем кнопки с вариантами ответов (обычные, без подсказок)
    keyboard = []
    for i, option in enumerate(task['options']):
        # Используем callback_data в формате: answer_<user_id>_<lang>_<task_id>_<option_index>
        callback_data = f"answer_{user_id}_{current_lang}_{task['id']}_{i}"
        keyboard.append([InlineKeyboardButton(f"{chr(65+i)}) {option}", callback_data=callback_data)])
    
    # Добавляем кнопки управления
    keyboard.append([
        InlineKeyboardButton("⏭ Пропустить", callback_data=f"skip_{user_id}_{current_lang}"),
        InlineKeyboardButton("ℹ️ Подсказка (2 ответа)", callback_data=f"hint_{user_id}_{current_lang}")
    ])
    
    # Добавляем кнопку смены языка
    keyboard.append([InlineKeyboardButton("🌍 Сменить язык", callback_data="change_language")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Формируем текст задачи
    task_text = f"""
    {lang_info['flag']} *Задача #{task['id']} из {lang_info['count']}* | Тип: {task['type']}
    ⭐ Язык: {lang_info['name']}
    
    *{task['question']}*
    
    Выберите правильный вариант ответа:
    
    ℹ️ *Подсказка:* уберет 2 неправильных варианта
    """
    
    # Если это сообщение с командой, отправляем новое сообщение
    if update.message:
        await update.message.reply_text(task_text, parse_mode='Markdown', reply_markup=reply_markup)
    # Если это callback query
    elif update.callback_query:
        await update.callback_query.edit_message_text(
            text=task_text,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )

# Функция для получения задачи с подсказкой
async def get_task_with_hint(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int, lang_key: str):
    if user_id not in user_stats or not user_stats[user_id]['current_task']:
        await update.callback_query.answer("Задача не найдена. Получите новую задачу.", show_alert=True)
        return
    
    task = user_stats[user_id]['current_task']
    lang_info = LANGUAGE_DATABASES[lang_key]
    
    # Увеличиваем счетчик использованных подсказок
    if 'used_hints' not in user_stats[user_id][lang_key]:
        user_stats[user_id][lang_key]['used_hints'] = 0
    user_stats[user_id][lang_key]['used_hints'] += 1
    
    # Находим индексы неправильных ответов (все кроме правильного)
    wrong_indices = [i for i in range(len(task['options'])) if i != task['correct_answer']]
    
    # Выбираем 2 случайных неправильных ответа для скрытия
    if len(wrong_indices) >= 2:
        hide_indices = random.sample(wrong_indices, 2)
    else:
        hide_indices = wrong_indices
    
    # Создаем кнопки с вариантами ответов (с подсказкой)
    keyboard = []
    for i, option in enumerate(task['options']):
        callback_data = f"answer_{user_id}_{lang_key}_{task['id']}_{i}"
        
        if i in hide_indices:
            # Скрываем неправильные варианты (делаем их перечеркнутыми)
            button_text = f"~~{chr(65+i)}) {option}~~"
            keyboard.append([InlineKeyboardButton(button_text, callback_data=callback_data)])
        else:
            # Показываем оставшиеся варианты
            button_text = f"{chr(65+i)}) {option}"
            keyboard.append([InlineKeyboardButton(button_text, callback_data=callback_data)])
    
    # Добавляем кнопки управления (теперь подсказка неактивна)
    keyboard.append([
        InlineKeyboardButton("⏭ Пропустить", callback_data=f"skip_{user_id}_{lang_key}"),
        InlineKeyboardButton("✅ Подсказка использована", callback_data="hint_used")
    ])
    
    # Добавляем кнопку смены языка
    keyboard.append([InlineKeyboardButton("🌍 Сменить язык", callback_data="change_language")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Формируем текст задачи с информацией о подсказке
    task_text = f"""
    {lang_info['flag']} *Задача #{task['id']} из {lang_info['count']}* | Тип: {task['type']}
    ⭐ Язык: {lang_info['name']}
    
    *{task['question']}*
    
    🎯 *Использована подсказка!* Убрано 2 неправильных варианта.
    
    Выберите правильный вариант из оставшихся:
    """
    
    await update.callback_query.edit_message_text(
        text=task_text,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

# Обработчик нажатия на кнопки
async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    # Обработка смены языка
    if data == "change_language":
        await show_language_selection(update, context)
        return
    
    # Обработка выбора языка
    if data.startswith("select_lang_"):
        lang_key = data.replace("select_lang_", "")
        user_id = update.effective_user.id
        
        if lang_key in LANGUAGE_DATABASES:
            user_languages[user_id] = lang_key
            lang_info = LANGUAGE_DATABASES[lang_key]
            
            # Создаем клавиатуру для возврата
            keyboard = [
                [InlineKeyboardButton("📚 Получить задачу", callback_data="get_task_callback")],
                [InlineKeyboardButton("📊 Статистика", callback_data="show_stats")]
            ]
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            confirmation_text = f"""
            ✅ *Язык изменен!*
            
            Теперь вы изучаете: {lang_info['flag']} {lang_info['name']}
            
            Доступно задач: {lang_info['count']}
            
            Начните обучение:
            """
            
            await query.edit_message_text(
                text=confirmation_text,
                parse_mode='Markdown',
                reply_markup=reply_markup
            )
        return
    
    # Обработка возврата к главному меню
    if data == "back_to_main":
        user_id = update.effective_user.id
        current_lang = user_languages.get(user_id, 'english')
        lang_info = LANGUAGE_DATABASES[current_lang]
        
        welcome_text = f"""
        🎓 *Language Learning Bot*
        
        🌍 *Текущий язык:* {lang_info['flag']} {lang_info['name']}
        📚 *Доступно задач:* {lang_info['count']}
        
        Выберите действие:
        """
        
        keyboard = [
            [InlineKeyboardButton("🌍 Сменить язык", callback_data="change_language")],
            [InlineKeyboardButton("📚 Получить задачу", callback_data="get_task_callback")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=welcome_text,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
        return
    
    # Получение задачи через callback
    if data == "get_task_callback":
        await get_task(update, context)
        return
    
    # Обработка подсказки - ОСНОВНОЕ ИСПРАВЛЕНИЕ!
    if data.startswith("hint_"):
        parts = data.split('_')
        if len(parts) >= 3:
            try:
                user_id = int(parts[1])
                lang_key = parts[2]
                
                # Проверяем, есть ли текущая задача
                if user_id in user_stats and user_stats[user_id]['current_task']:
                    # Получаем задачу с подсказкой
                    await get_task_with_hint(update, context, user_id, lang_key)
                else:
                    await query.answer("Сначала получите задачу!", show_alert=True)
            except ValueError:
                await query.answer("Ошибка обработки подсказки", show_alert=True)
        else:
            await query.answer("Некорректные данные подсказки", show_alert=True)
        return
    
    # Обработка использованной подсказки
    if data == "hint_used":
        await query.answer("Вы уже использовали подсказку для этой задачи!", show_alert=True)
        return
    
    # Обработка пропуска задачи
    if data.startswith("skip_"):
        parts = data.split('_')
        if len(parts) >= 3:
            user_id = int(parts[1])
            lang_key = parts[2]
            
            if user_id in user_stats and user_stats[user_id]['current_task']:
                task = user_stats[user_id]['current_task']
                lang_info = LANGUAGE_DATABASES[lang_key]
                correct_answer = task['options'][task['correct_answer']]
                explanation = task['explanation']
                
                # Обновляем статистику
                user_stats[user_id][lang_key]['total'] += 1
                
                result_text = f"""
                {lang_info['flag']} ⏭ *Задача #{task['id']} пропущена*
                
                *Правильный ответ:* {correct_answer}
                
                *Объяснение:* {explanation}
                
                *Язык:* {lang_info['name']}
                
                Выберите действие:
                """
                
                # Создаем кнопки для продолжения
                keyboard = [
                    [InlineKeyboardButton("🔄 Новая задача", callback_data="new_task")],
                    [InlineKeyboardButton("📊 Статистика", callback_data="show_stats")],
                    [InlineKeyboardButton("🌍 Сменить язык", callback_data="change_language")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await query.edit_message_text(
                    text=result_text,
                    parse_mode='Markdown',
                    reply_markup=reply_markup
                )
        return
    
    # Обработка ответа на задачу
    if data.startswith("answer_"):
        parts = data.split('_')
        if len(parts) >= 5:
            try:
                user_id = int(parts[1])
                lang_key = parts[2]
                task_id = int(parts[3])
                selected_option = int(parts[4])
                
                # Ищем задачу в базе данных
                lang_info = LANGUAGE_DATABASES[lang_key]
                task = None
                for t in lang_info['tasks']:
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
                    user_stats[user_id] = {
                        'english': {'correct': 0, 'total': 0, 'used_hints': 0}, 
                        'german': {'correct': 0, 'total': 0, 'used_hints': 0}, 
                        'current_task': None
                    }
                
                user_stats[user_id][lang_key]['total'] += 1
                if is_correct:
                    user_stats[user_id][lang_key]['correct'] += 1
                
                # Формируем ответ
                if is_correct:
                    result_icon = "✅"
                    result_text = "ПРАВИЛЬНО! Отличная работа!"
                else:
                    result_icon = "❌"
                    result_text = "НЕПРАВИЛЬНО! Попробуйте еще раз!"
                
                # Рассчитываем процент успеха для текущего языка
                stats = user_stats[user_id][lang_key]
                success_rate = 0
                if stats['total'] > 0:
                    success_rate = (stats['correct'] / stats['total']) * 100
                
                # Создаем кнопки для продолжения
                keyboard = [
                    [InlineKeyboardButton("🔄 Новая задача", callback_data="new_task")],
                    [
                        InlineKeyboardButton("📊 Статистика", callback_data="show_stats"),
                        InlineKeyboardButton("🌍 Сменить язык", callback_data="change_language")
                    ]
                ]
                
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                # Добавляем информацию о подсказках, если они использовались
                hints_used = stats.get('used_hints', 0)
                hints_info = f"\n*Использовано подсказок:* {hints_used}" if hints_used > 0 else ""
                
                response_text = f"""
                {result_icon} *{result_text}*
                
                {lang_info['flag']} *Задача #{task['id']}* | Язык: {lang_info['name']}
                
                *Ваш ответ:* {selected_answer}
                *Правильный ответ:* {correct_answer}
                
                *Объяснение:* {explanation}
                
                *Статистика по {lang_info['name']}:* {stats['correct']}/{stats['total']} правильных ответов{hints_info}
                *Успешность:* {success_rate:.1f}%
                
                Выберите действие:
                """
                
                # Сохраняем данные в контексте
                context.user_data['last_user_id'] = user_id
                context.user_data['last_lang'] = lang_key
                
                await query.edit_message_text(
                    text=response_text,
                    parse_mode='Markdown',
                    reply_markup=reply_markup
                )
            except (ValueError, IndexError) as e:
                await query.edit_message_text(f"Ошибка обработки ответа: {str(e)}")
    
    # Новая задача
    elif data == "new_task":
        user_id = context.user_data.get('last_user_id', update.effective_user.id)
        lang_key = context.user_data.get('last_lang', user_languages.get(user_id, 'english'))
        
        if user_id in user_stats:
            user_stats[user_id]['current_task'] = None
        
        # Устанавливаем язык для пользователя
        user_languages[user_id] = lang_key
        
        # Отправляем новую задачу
        await get_task(update, context)
    
    # Показать статистику
    elif data == "show_stats":
        await show_stats_callback(update, context)
    
    # Показать общую статистику
    elif data == "show_all_stats":
        await show_all_stats_callback(update, context)

# Команда /stats
async def show_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id not in user_stats:
        await update.message.reply_text("📊 У вас еще нет статистики. Решите несколько задач: /task")
        return
    
    # Создаем текст статистики
    stats_text = await get_user_stats_text(user_id)
    
    # Добавляем кнопку смены языка
    keyboard = [
        [InlineKeyboardButton("🌍 Сменить язык", callback_data="change_language")],
        [InlineKeyboardButton("📚 Получить задачу", callback_data="get_task_callback")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(stats_text, parse_mode='Markdown', reply_markup=reply_markup)

# Функция для получения текста статистики
async def get_user_stats_text(user_id):
    if user_id not in user_stats:
        return "📊 У вас еще нет статистики."
    
    stats_text = "📊 *Ваша статистика по всем языкам:*\n\n"
    has_stats = False
    
    for lang_key, lang_data in LANGUAGE_DATABASES.items():
        # Проверяем, есть ли статистика для этого языка
        if lang_key in user_stats[user_id]:
            stats = user_stats[user_id][lang_key]
        else:
            stats = {'correct': 0, 'total': 0, 'used_hints': 0}
        
        if stats['total'] > 0:
            has_stats = True
            success_rate = (stats['correct'] / stats['total']) * 100 if stats['total'] > 0 else 0
            
            # Определяем уровень
            level = get_user_level(success_rate)
            
            stats_text += f"{lang_data['flag']} *{lang_data['name']}:*\n"
            stats_text += f"✓ Решено: {stats['correct']} из {stats['total']}\n"
            stats_text += f"📈 Успешность: {success_rate:.1f}%\n"
            stats_text += f"🏅 Уровень: {level['name']} {level['emoji']}\n"
            
            # Добавляем информацию о подсказках
            hints_used = stats.get('used_hints', 0)
            if hints_used > 0:
                stats_text += f"💡 Использовано подсказок: {hints_used}\n"
            
            # Добавляем прогресс-бар
            progress = min(stats['total'], lang_data['count'])
            progress_bar = create_progress_bar(progress, lang_data['count'])
            stats_text += f"📊 Прогресс: {progress_bar} {progress}/{lang_data['count']}\n\n"
    
    # Если нет статистики ни по одному языку
    if not has_stats:
        stats_text = "📊 У вас еще нет статистики. Решите несколько задач: /task"
    else:
        # Добавляем общую информацию
        total_correct = sum(user_stats[user_id].get(lang, {'correct': 0})['correct'] for lang in LANGUAGE_DATABASES.keys())
        total_all = sum(user_stats[user_id].get(lang, {'total': 0})['total'] for lang in LANGUAGE_DATABASES.keys())
        total_hints = sum(user_stats[user_id].get(lang, {'used_hints': 0})['used_hints'] for lang in LANGUAGE_DATABASES.keys())
        
        if total_all > 0:
            overall_rate = (total_correct / total_all) * 100
            stats_text += f"━━━━━━━━━━━━━━━━━━━━\n"
            stats_text += f"🌍 *Общая статистика:*\n"
            stats_text += f"✓ Всего решено: {total_correct} из {total_all}\n"
            stats_text += f"📈 Общая успешность: {overall_rate:.1f}%\n"
            if total_hints > 0:
                stats_text += f"💡 Всего подсказок: {total_hints}\n"
            
            # Текущий язык
            current_lang = user_languages.get(user_id, 'english')
            lang_info = LANGUAGE_DATABASES[current_lang]
            stats_text += f"🎯 *Текущий язык:* {lang_info['flag']} {lang_info['name']}\n"
    
    return stats_text

# Callback для статистики
async def show_stats_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    # Получаем текст статистики
    stats_text = await get_user_stats_text(user_id)
    
    # Создаем кнопки
    keyboard = [
        [InlineKeyboardButton("🔄 Новая задача", callback_data="new_task")],
        [
            InlineKeyboardButton("🌍 Сменить язык", callback_data="change_language"),
            InlineKeyboardButton("📖 Темы", callback_data="show_topics_callback")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=stats_text,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

# Callback для общей статистики
async def show_all_stats_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    # Получаем текст статистики
    stats_text = await get_user_stats_text(user_id)
    
    # Создаем кнопки
    keyboard = [
        [InlineKeyboardButton("🔄 Новая задача", callback_data="new_task")],
        [InlineKeyboardButton("🌍 Сменить язык", callback_data="change_language")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=stats_text,
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
    if total == 0:
        return '░' * length
    
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

# Токен бота
TOKEN = "YOUR_TOKEN_BOT"

# Создаем приложение
application = Application.builder().token(TOKEN).build()

# Регистрируем обработчики команд
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("task", get_task))
application.add_handler(CommandHandler("stats", show_stats))
application.add_handler(CommandHandler("language", change_language_command))

# Регистрируем обработчики callback query
application.add_handler(CallbackQueryHandler(handle_answer))

# Регистрируем обработчик ошибок
application.add_error_handler(error_handler)

# Запускаем бота
print("Бот запущен...")
print(f"Доступные языки: {len(LANGUAGE_DATABASES)}")
for lang_key, lang_data in LANGUAGE_DATABASES.items():
    print(f"  {lang_data['flag']} {lang_data['name']}: {lang_data['count']} задач")
application.run_polling(allowed_updates=Update.ALL_TYPES)