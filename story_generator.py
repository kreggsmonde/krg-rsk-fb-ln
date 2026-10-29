import os, sys, json, time, requests, re
import config

RELATIONSHIP_CURRICULUM = [['Секреты эмоциональной привязанности', 'Понять наши стили привязанности и глубинные страхи, чтобы любить в безопасности'], ['Искусство говорить не раня', 'Выражать потребности с нежностью и ясностью, без упрёков и защиты'], ['Учимся выстраивать здоровые границы', 'Говорить «нет» доброжелательно, сохраняя гармонию пары и самооценку'], ['Исцеление страха отвержения и одиночества', 'Вернуть внутреннюю опору и построить непоколебимое доверие в отношениях'], ['5 языков любви в повседневности', 'Расшифровать глубинные эмоциональные потребности партнёра и питать любовь каждый день'], ['Уязвимость: невидимая сила пары', 'Почему смелость быть настоящим и несовершенным — единственный ключ к близости'], ['Разряжать конфликты без обиды', 'Превращать разногласия в возможности сближения и взаимопонимания'], ['Выход из эмоциональной зависимости', 'Как взрастить эмоциональную самостоятельность и расцвести вдвоём'], ['Активное слушание и сила тишины', 'Услышать то, что сердце другого шепчет сквозь усталость и будничные слова'], ['Восстановление доверия после раны', 'Терпеливый путь исправления, правды и общего прощения']]

DEFAULT_5_ACTS = [['Акт 1: Диагноз сердца', 'Тёплое вступление и погружение в реальность проблемы отношений'], ['Акт 2: Бессознательные корни', 'Психологическое исследование страхов, детских ран и наших защитных реакций'], ['Акт 3: Практические ключи и успокаивающие слова', 'Преображающие фразы, доброжелательные установки и конструктивные повседневные диалоги'], ['Акт 4: Проходя через эмоциональные бури', 'Проживать гнев и замкнутость, преодолевать напряжение без паники'], ['Акт 5: Упражнение сердца и ежедневное благословение', 'Доброжелательное задание для саморефлексии, ритуал связи на неделю и послание надежды']]

def load_history_topics() -> list:
    """Reads all past published topics from published_videos.json and history.json to ensure no repeats."""
    past = []
    for fname in ["published_videos.json", "history.json"]:
        fpath = os.path.join(config.BASE_DIR, fname)
        if os.path.exists(fpath):
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        for item in data:
                            if isinstance(item, dict) and item.get("topic"):
                                t = item["topic"].strip()
                                if t not in past:
                                    past.append(t)
            except Exception:
                pass
    return past

def generate_dynamic_topic_ai(past_topics: list, ep_num: int = 1) -> dict:
    """Запрашивает Pollinations AI с историей прошлых тем совершенно новую, неповторяющуюся русскую тему об отношениях."""
    key = config.POLLINATIONS_API_KEY
    if not key:
        return None

    past_sample = past_topics[-30:] if len(past_topics) > 30 else past_topics
    prompt = (
        f"Ты — исполнительный продюсер и автор концепции русского подкаста '{config.CHANNEL_NAME}'.\n"
        f"Слоган: {config.TAGLINE}\n"
        f"Формат: Интимный сольный подкаст с {config.HOST1_NAME}, доброжелательным психологом и доверенным собеседником.\n"
        f"Тематика: Человеческие отношения, психология любви, привязанность, общение, нежность, устойчивость пары.\n"
        f"Языковое правило: ВСЁ должно быть написано элегантным, естественным и тёплым русским языком.\n\n"
        f"Уже разобранные выпуски (НЕ ПОВТОРЯТЬ):\n"
        + json.dumps(past_sample, indent=2, ensure_ascii=False) + "\n\n"
        f"Сгенерируй ОДНУ НОВУЮ, увлекательную и обогащающую тему выпуска #{ep_num}.\n\n"
        f"ФОРМАТ ВЫВОДА: Верни ИСКЛЮЧИТЕЛЬНО валидный JSON-объект (без markdown снаружи, без вступления):\n"
        "{\n"
        f'  "id": "ep_{ep_num}",\n'
        '  "topic": "Увлекательное русское название (напр.: Научиться прощать не забывая о себе)",\n'
        '  "focus": "Одно предложение: что слушатель поймёт и преобразит в своих привязанностях",\n'
        '  "thumbnail_title_1": "ПЕРВЫЕ СЛОВА (МАКС. 16 СИМВОЛОВ)",\n'
        '  "thumbnail_title_2": "ВТОРЫЕ СЛОВА (МАКС. 16 СИМВОЛОВ)",\n'
        '  "thumbnail_hook": "Цепляющий хук (напр.: Мягко спасти пару)",\n'
        '  "acts": [\n'
        '    ["Акт 1: Название", "Описание фокуса акта..."],\n'
        '    ["Акт 2: Название", "Описание фокуса акта..."],\n'
        '    ["Акт 3: Название", "Описание фокуса акта..."],\n'
        '    ["Акт 4: Название", "Описание фокуса акта..."],\n'
        '    ["Акт 5: Название", "Описание фокуса акта..."]\n'
        '  ]\n'
        "}" 
    )

    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    payload = {
        "model": config.POLLINATIONS_MODEL,
        "messages": [
            {"role": "system", "content": "Ты — первоклассный продюсер подкастов. Отвечаешь исключительно валидным JSON."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.82
    }

    for attempt in range(3):
        try:
            print(f"[StoryGenerator] ИИ-синтез новой темы об отношениях (попытка {attempt+1}/3)...")
            resp = requests.post(config.POLLINATIONS_ENDPOINT, json=payload, headers=headers, timeout=25)
            if resp.status_code == 200:
                raw = resp.json()["choices"][0]["message"]["content"].strip()
                if "```" in raw:
                    raw = raw.split("```")[1]
                    if raw.startswith("json"):
                        raw = raw[4:].strip()
                    raw = raw.split("```")[0].strip()
                data = json.loads(raw)
                topic_val = data.get("topic", "")
                if topic_val and data.get("acts") and len(data["acts"]) >= 4:
                    t_lower = topic_val.lower().strip()
                    past_lowers = [p.lower().strip() for p in past_topics]
                    if t_lower not in past_lowers:
                        print(f"[StoryGenerator] Новая тема успешно сгенерирована: '{topic_val}'")
                        return data
        except Exception as e:
            print(f"[StoryGenerator] Ошибка ИИ-попытки темы ({attempt+1}) : {e}")
            time.sleep(1.5)
    return None

def get_next_topic(history: list, custom_topic: str = None, ep_num: int = 1) -> dict:
    if custom_topic:
        words = custom_topic.split()
        mid = len(words) // 2
        t1 = " ".join(words[:mid]) if mid > 0 else words[0]
        t2 = " ".join(words[mid:]) if mid > 0 else "ОТНОШЕНИЯ"
        return {
            "id": f"custom_{ep_num}",
            "topic": custom_topic,
            "focus": "Интимное и успокаивающее размышление о динамике человеческих отношений",
            "thumbnail_title_1": t1[:16].upper(),
            "thumbnail_title_2": t2[:16].upper(),
            "thumbnail_hook": "Понять сердце",
            "acts": DEFAULT_5_ACTS
        }

    past_topics = load_history_topics()

    # 1. AI Dynamic Generation
    ai_topic = generate_dynamic_topic_ai(past_topics, ep_num=ep_num)
    if ai_topic:
        t1 = ai_topic.get("thumbnail_title_1", "")
        t2 = ai_topic.get("thumbnail_title_2", "")
        if not t1 or not t2:
            words = ai_topic["topic"].split()
            mid = len(words) // 2
            t1 = " ".join(words[:mid])
            t2 = " ".join(words[mid:])
        return {
            "id": ai_topic.get("id", f"ep_{ep_num}"),
            "topic": ai_topic["topic"],
            "focus": ai_topic.get("focus", "Понять и питать наши эмоциональные отношения"),
            "thumbnail_title_1": t1[:16].upper(),
            "thumbnail_title_2": t2[:16].upper(),
            "thumbnail_hook": ai_topic.get("thumbnail_hook", "Психология пары"),
            "acts": ai_topic.get("acts", DEFAULT_5_ACTS)
        }

    # 2. Curated Curriculum Fallback
    past_lowers = [p.lower().strip() for p in past_topics]
    for idx, (title, focus) in enumerate(RELATIONSHIP_CURRICULUM):
        if title.lower().strip() not in past_lowers:
            print(f"[StoryGenerator] Выбрана тема из каталога: '{title}'")
            words = title.split()
            mid = len(words) // 2
            t1 = " ".join(words[:mid])
            t2 = " ".join(words[mid:])
            return {
                "id": f"ep_{ep_num}",
                "topic": title,
                "focus": focus,
                "thumbnail_title_1": t1[:16].upper(),
                "thumbnail_title_2": t2[:16].upper(),
                "thumbnail_hook": "Искусство человеческих отношений",
                "acts": DEFAULT_5_ACTS
            }

    # 3. Endless Cycle Variation
    cycle = (ep_num - 1) // len(RELATIONSHIP_CURRICULUM) + 1
    cat_idx = (ep_num - 1) % len(RELATIONSHIP_CURRICULUM)
    base_title, base_focus = RELATIONSHIP_CURRICULUM[cat_idx]
    title = f"{base_title} : Углубление и исцеление (часть {cycle})"
    words = title.split()
    mid = len(words) // 2
    t1 = " ".join(words[:mid])
    t2 = " ".join(words[mid:])
    return {
        "id": f"ep_{ep_num}",
        "topic": title,
        "focus": f"Существенное углубление: {base_focus}",
        "thumbnail_title_1": t1[:16].upper(),
        "thumbnail_title_2": t2[:16].upper(),
        "thumbnail_hook": f"Терапевтический подход #{cycle}",
        "acts": DEFAULT_5_ACTS
    }

def generate_curated_fallback_act(act_idx: int, act_title: str, topic: str, target_turns: int = 40) -> list:
    """Русские монологи об отношениях с терапевтическим теплом и поэтической элегантностью."""
    h1 = config.HOST1_NAME
    s1 = config.HOST1_SPEAKER
    cname = config.CHANNEL_NAME

    solo_act_scripts = [
        # Акт 1: Диагноз сердца
        [
        f"Добро пожаловать в {cname}. Я очень рада, что вы сегодня со мной в эту интимную минуту.",
        f"Сегодня мы остановимся и уделим время важной теме: {topic}.",
        f"В суете повседневности мы часто забываем прислушаться к биению собственного сердца.",
        f"Человеческие отношения — одновременно наше величайшее убежище и честнейшее зеркало.",
        f"Когда мы любим, мы обнажаем глубочайшие желания, но и хрупкость.",
        f"Возможно, вам знакомо это тихое непонимание, что порой поселяется между двумя людьми.",
        f"Двое, которые глубоко любят друг друга, и больше не могут понять друг друга.",
        f"Сделайте вместе со мной глубокий вдох и отпустите всё накопленное напряжение.",
        f"Этот подкаст — ваше святилище, место, где уязвимость становится огромной силой.",
        f"Мы здесь не ради совершенства и не ради упрёков.",
        ],
        # Акт 2: Бессознательные корни
        [
        f"Чтобы понять происходящее в наших сегодняшних отношениях, часто нужно оглянуться назад.",
        f"Наша манера любить и привязываться берёт начало в самых ранних детских переживаниях.",
        f"Именно первые семейные связи сформировали наш эмоциональный компас.",
        f"Там, где не хватало безопасности, может рождаться панический страх одиночества.",
        f"Эти бессознательные реакции — наши стили привязанности, наши защитные доспехи.",
        f"Когда партнёр отдаляется, чтобы передохнуть, наш внутренний ребёнок паникует.",
        f"Нам кажется, что любовь исчезает, а человеку просто нужно пространство.",
        f"Это понимание меняет абсолютно всё в динамике пары.",
        f"Гнев — часто лишь отчаянный призыв быть увиденным и успокоенным.",
        f"Когда за маской равнодушия мы видим хрупкость, нежность возрождается.",
        ],
        # Акт 3: Практические ключи и успокаивающие слова
        [
        f"Перейдём теперь к ежедневной практике этого общения сердца.",
        f"Главная ловушка разговора: атаковать личность другого вместо того, чтобы выразить свои чувства.",
        f"Замените 'Ты никогда меня не слушаешь' простым 'Мне сейчас одиноко'.",
        f"Заметьте, как этот маленький нюанс мгновенно снимает потребность в контратаке.",
        f"Кто говорит о себе, честно и уязвимо, тот приглашает другого утешить.",
        f"Кто обвиняет, тот заставляет другого надевать доспехи.",
        f"Ещё один чудесный секрет — искусство маленьких неожиданных знаков внимания.",
        f"Эти крошечные жесты посылают нервной системе мощный сигнал: со мной ты в безопасности.",
        f"Не ждите больших годовщин, чтобы отпраздновать присутствие любимого человека.",
        f"Скажите сегодня просто 'Я понимаю тебя, и я рядом', в этом бесконечная целительная сила.",
        ],
        # Акт 4: Проходя через эмоциональные бури
        [
        f"Даже при величайшей мудрости бури и трения — часть жизни вдвоём.",
        f"Двое, делящие быт, неизбежно переживают моменты разногласий и усталости.",
        f"Секрет прочных пар не в отсутствии конфликтов, а в умении их проходить.",
        f"Когда напряжение растёт, а тон обостряется, наш мозг переходит в режим выживания.",
        f"В тревожном состоянии невозможен ни один конструктивный разговор.",
        f"Самый смелый шаг — успокаивающая пауза: 'Я люблю тебя, давай десять минут подышим'.",
        f"Такая передышка замедляет сердце и спасает от ранящих слов, о которых жалеют.",
        f"Гордость и эго — худшие советчики, когда речь о любви.",
        f"Спросите себя: вам важнее быть правым любой ценой, или быть в мире и связи?",
        f"Признать собственные ошибки — никогда не слабость, а вершина элегантности сердца.",
        ],
        # Акт 5: Упражнение сердца и ежедневное благословение
        [
        f"Вот мы и подошли к концу нашего совместного размышления на этом канале.",
        f"Чтобы закрепить это понимание в жизни, предлагаю вам упражнение сердца на неделю.",
        f"Сегодня или завтра скажите близкому человеку, какую красоту дарит вам его присутствие.",
        f"Говорите не о том, что он делает, а о том, кто он для вас и какой свет излучает.",
        f"Вы увидите, как искреннее слово озаряет лицо и согревает целый день.",
        f"Помните: вы достойны любви с уважением, мягкостью и вниманием.",
        f"Бесконечно благодарю вас за внимание и верность на {cname}.",
        f"Подпишитесь, чтобы не пропустить ни одной нашей мягкой и проясняющей встречи.",
        f"Берегите себя и близких и всегда взращивайте драгоценное искусство отношений.",
        f"До скорой встречи в новом выпуске, полном нежности и ясности.",
        ],
    ]

    safe_act_idx = min(act_idx, len(solo_act_scripts) - 1)
    lines = solo_act_scripts[safe_act_idx]
    result = []
    for l in lines:
        result.append({"speaker": s1, "name": h1, "text": l})
        if len(result) >= target_turns:
            break

    while len(result) < target_turns:
        for l in lines:
            prefix = "Размышляя об этом сердцем, "
            result.append({"speaker": s1, "name": h1, "text": f"{prefix}{l[0].lower() + l[1:] if len(l) > 1 else l}"})
            if len(result) >= target_turns:
                break

    return result

def generate_act_ai(act_idx: int, act_title: str, topic_title: str, focus: str, target_turns: int = 35) -> list:
    key = config.POLLINATIONS_API_KEY
    if not key:
        return None

    if act_idx == 0:
        transition_note = "Открывающий акт: тепло поприветствуй слушателя на канале, создай мягкую, интимную атмосферу и чутко введи в тему."
    elif act_idx == 1:
        transition_note = "Акт 2: ВАЖНО - НЕ говори «добро пожаловать». Продолжи прямо и естественно к психологическим корням и бессознательному."
    elif act_idx == 2:
        transition_note = "Акт 3: ВАЖНО - НЕ говори «добро пожаловать». Плавно перейди к конкретным повседневным примерам, мягкому общению и успокаивающим словам."
    elif act_idx == 3:
        transition_note = "Акт 4: ВАЖНО - НЕ говори «добро пожаловать». Продолжи про проживание кризисов, ссор и исцеление ран без паники."
    else:
        transition_note = "Акт 5 (финал): ВАЖНО - Мягкий переход к практическому заданию недели, посланию надежды для пары и тёплому заключению."

    prompt = (
        f"Ты пишешь сценарий интимного и утешающего выпуска подкаста для канала '{config.CHANNEL_NAME}'.\n"
        f"Единственная ведущая: {config.HOST1_NAME} (психолог и специалист по человеческим отношениям, тёплый, эмпатичный и доброжелательный женский голос).\n"
        f"Формат: СОЛО-МОНОЛОГ на русском, где она обращается напрямую к слушателю ('вы') как к дорогому другу или в интимной консультации.\n"
        f"Тема выпуска: {topic_title}\n"
        f"Текущий раздел: {act_title}\n"
        f"Эмоциональный фокус: {focus}\n"
        f"Правило перехода: {transition_note}\n\n"
        f"СТРОГИЕ ТРЕБОВАНИЯ:\n"
        f"- Ровно {target_turns} последовательных реплик монолога от {config.HOST1_NAME}.\n"
        f"- Каждая реплика 14–24 слова, в естественном, плавном, трогательном и элегантном разговорном стиле.\n"
        f"- Психологическая лексика доступная, полная доброжелательности, нюансов и эмоциональной мудрости.\n"
        f"- Верни ИСКЛЮЧИТЕЛЬНО сырой JSON-массив объектов (без markdown, без сопроводительного текста):\n"
        f"[\n"
        f"- Каждый объект ДОЛЖЕН также содержать поле \"en\" с естественным переводом поля \"text\" на английский язык (только субтитры, никогда не произносится).\n"
        f'  {{"speaker": "{config.HOST1_SPEAKER}", "name": "{config.HOST1_NAME}", "text": "...", "en": "..."}},\n'
        f'  {{"speaker": "{config.HOST1_SPEAKER}", "name": "{config.HOST1_NAME}", "text": "...", "en": "..."}}\n'
        f"]"
    )

    try:
        resp = requests.post(
            config.POLLINATIONS_ENDPOINT,
            json={
                "model": config.POLLINATIONS_MODEL,
                "messages": [
                    {"role": "system", "content": "Ты — первоклассный генератор радиоэфиров и подкастов. Отвечаешь исключительно валидным JSON."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.78
            },
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            timeout=25
        )
        if resp.status_code == 200:
            raw = resp.json()["choices"][0]["message"]["content"].strip()
            if "```" in raw:
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:].strip()
                raw = raw.split("```")[0].strip()
            parsed = json.loads(raw)
            min_needed = max(2, min(target_turns, 8))
            if isinstance(parsed, list) and len(parsed) >= min_needed:
                result_turns = []
                for p in parsed:
                    txt = p.get("text", "").strip()
                    if not txt:
                        continue
                    result_turns.append({"speaker": config.HOST1_SPEAKER, "name": config.HOST1_NAME, "text": txt, "en": p.get("en", "").strip()})

                # Sanitize repetitive greetings in Acts 2-5
                if act_idx > 0 and result_turns:
                    first_text = result_turns[0]["text"]
                    for prefix in ['добро пожаловать', 'здравствуйте и добро пожаловать', 'снова здравствуйте', 'всем привет']:
                        if first_text.lower().startswith(prefix):
                            cleaned = re.sub(r"^(?:добро пожаловать(?:\s+снова)?(?:\s+на\s+[^.!?]*)?[.!?]\s*|здравствуйте[^.!?]*[.!?]\s*|всем привет[^.!?]*[.!?]\s*)", "", first_text, flags=re.IGNORECASE).strip()
                            if cleaned:
                                result_turns[0]["text"] = cleaned[0].upper() + cleaned[1:] if len(cleaned) > 1 else cleaned
                            else:
                                result_turns[0]["text"] = f"Продолжим наше размышление о {topic_title}, взглянув на наше повседневное поведение."
                            break

                if len(result_turns) >= target_turns:
                    return result_turns[:target_turns]
                elif len(result_turns) >= min_needed:
                    fallback_turns = generate_curated_fallback_act(act_idx, act_title, topic_title, target_turns=target_turns)
                    seen_texts = set(r["text"] for r in result_turns)
                    for ft in fallback_turns:
                        if len(result_turns) >= target_turns:
                            break
                        if ft["text"] not in seen_texts:
                            result_turns.append(ft)
                            seen_texts.add(ft["text"])
                    return result_turns[:target_turns]
    except Exception as e:
        print(f"  [ИИ-примечание] Акт {act_idx+1} перешёл на курированный резервный сценарий: {e}")
    return None

def generate_full_podcast_story(target_minutes: float = 20.0, topic: str = None, ep_num: int = 1) -> dict:
    history = load_history_topics()
    topic_info = get_next_topic(history, custom_topic=topic, ep_num=ep_num)
    selected_topic = topic_info["topic"]
    acts_meta = topic_info.get("acts", DEFAULT_5_ACTS)

    print(f"[StoryGenerator] Выпуск #{ep_num} - Тема: '{selected_topic}'")

    # Target 20 minutes calibrated with slower -6% speech rate and 0.75s natural pauses (~6.5s per turn)
    turns_per_act = int(max(4, (target_minutes * 60) / (len(acts_meta) * 6.5)))
    if target_minutes <= 1.0:
        turns_per_act = 4
    elif target_minutes <= 3.0:
        turns_per_act = 8

    dialogue = []
    chapters = []

    for act_idx, (act_title, act_focus) in enumerate(acts_meta):
        chapters.append({"title": act_title, "start_turn": len(dialogue)})
        print(f"  [Акт {act_idx+1}/5] Генерация '{act_title}' ({turns_per_act} реплик)...")

        turns = generate_act_ai(act_idx, act_title, selected_topic, act_focus, target_turns=turns_per_act)
        if not turns:
            turns = generate_curated_fallback_act(act_idx, act_title, selected_topic, target_turns=turns_per_act)

        dialogue.extend(turns)

    print(f"[StoryGenerator] Полный монолог сгенерирован: {len(dialogue)} реплик в {len(acts_meta)} актах.")
    return {
        "topic": selected_topic,
        "thumbnail_title_1": topic_info["thumbnail_title_1"],
        "thumbnail_title_2": topic_info["thumbnail_title_2"],
        "thumbnail_hook": topic_info["thumbnail_hook"],
        "chapters": chapters,
        "dialogue": dialogue
    }

def generate_metadata(topic: str, duration_sec: float, chapters: list, ep_num: int = 1) -> dict:
    title = f"{topic} | {config.CHANNEL_NAME} Вып. {ep_num}"
    lines = [
        f"🎙️ Добро пожаловать в {config.CHANNEL_NAME} с {config.HOST1_NAME} - Выпуск #{ep_num}!",
        f"Тема дня: {topic}",
        "",
        "🕒 ГЛАВЫ И МЕТКИ ВРЕМЕНИ:",
    ]
    for ch in chapters:
        m = int(ch.get("start_time", 0) // 60)
        s = int(ch.get("start_time", 0) % 60)
        lines.append(f"{m:02d}:{s:02d} - {ch['title']}")

    clean_tag = config.CHANNEL_NAME.replace(" ", "").replace("'", "")
    lines.extend([
        "",
        "💡 Мягкое и проясняющее путешествие в сердце психологии человеческих отношений, любви и эмоциональной близости.",
        "👉 Подпишитесь, чтобы каждую неделю получать новый успокаивающий и вдохновляющий выпуск.",
    f"#{clean_tag} #Психология #Отношения #Любовь #Подкаст #Саморазвитие #Привязанность"
    ])

    return {
        "title": title[:100],
        "description": "\n".join(lines),
        "tags": ["человеческие отношения", "психология пары", "подкаст", "любовь", "доброжелательное общение", "эмоциональная привязанность", config.CHANNEL_NAME.lower()]
    }
