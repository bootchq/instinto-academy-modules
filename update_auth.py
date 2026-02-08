#!/usr/bin/env python3
"""Добавляет авторизацию и тесты в HTML."""

import re
from pathlib import Path

HTML_FILE = Path("/private/tmp/academy-modules/index.html")

# Новые CSS стили
NEW_CSS = '''
        /* Login Screen */
        .login-screen {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 2000;
        }

        .login-screen.hidden {
            display: none;
        }

        .login-box {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 20px;
            padding: 40px;
            max-width: 400px;
            width: 90%;
            text-align: center;
        }

        .login-box h2 {
            color: #e94560;
            margin-bottom: 10px;
            font-size: 1.8rem;
        }

        .login-box p {
            color: #8892b0;
            margin-bottom: 30px;
        }

        .login-input {
            width: 100%;
            padding: 15px 20px;
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 10px;
            background: rgba(255,255,255,0.05);
            color: #e8e8e8;
            font-size: 1rem;
            margin-bottom: 15px;
            outline: none;
            transition: border-color 0.3s;
        }

        .login-input:focus {
            border-color: #e94560;
        }

        .login-btn {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #e94560, #ff6b6b);
            border: none;
            border-radius: 10px;
            color: white;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.3s, box-shadow 0.3s;
        }

        .login-btn:hover {
            transform: scale(1.02);
            box-shadow: 0 5px 20px rgba(233, 69, 96, 0.4);
        }

        .login-error {
            color: #ff4757;
            margin-top: 15px;
            display: none;
        }

        /* Locked module */
        .module.locked {
            opacity: 0.5;
            pointer-events: none;
        }

        .module.locked .module-header {
            cursor: not-allowed;
        }

        .module-lock {
            color: #8892b0;
            font-size: 1.2rem;
            margin-left: auto;
        }

        .module.locked .module-toggle {
            display: none;
        }

        /* Progress badge */
        .badge-progress {
            background: rgba(233, 69, 96, 0.2);
            color: #e94560;
        }

        .badge-passed {
            background: rgba(46, 213, 115, 0.2);
            color: #2ed573;
        }

        /* Quiz styles */
        .quiz-container {
            margin-top: 40px;
            padding-top: 30px;
            border-top: 2px solid rgba(233, 69, 96, 0.3);
        }

        .quiz-title {
            font-size: 1.5rem;
            color: #e94560;
            margin-bottom: 20px;
            text-align: center;
        }

        .quiz-progress {
            text-align: center;
            color: #8892b0;
            margin-bottom: 20px;
        }

        .quiz-question {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 20px;
        }

        .quiz-question-text {
            font-size: 1.1rem;
            color: #ccd6f6;
            margin-bottom: 20px;
        }

        .quiz-options {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .quiz-option {
            padding: 15px 20px;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
            color: #a8b2d1;
        }

        .quiz-option:hover {
            background: rgba(233, 69, 96, 0.1);
            border-color: rgba(233, 69, 96, 0.3);
        }

        .quiz-option.selected {
            background: rgba(233, 69, 96, 0.2);
            border-color: #e94560;
            color: #e8e8e8;
        }

        .quiz-option.correct {
            background: rgba(46, 213, 115, 0.2);
            border-color: #2ed573;
            color: #2ed573;
        }

        .quiz-option.wrong {
            background: rgba(255, 71, 87, 0.2);
            border-color: #ff4757;
            color: #ff4757;
        }

        .quiz-nav {
            display: flex;
            justify-content: space-between;
            margin-top: 20px;
        }

        .quiz-btn {
            padding: 12px 25px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1rem;
            transition: all 0.3s;
        }

        .quiz-btn-next {
            background: linear-gradient(135deg, #e94560, #ff6b6b);
            border: none;
            color: white;
        }

        .quiz-btn-next:hover {
            transform: scale(1.05);
        }

        .quiz-btn-next:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }

        .quiz-result {
            text-align: center;
            padding: 40px;
        }

        .quiz-result-score {
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 10px;
        }

        .quiz-result-score.pass {
            color: #2ed573;
        }

        .quiz-result-score.fail {
            color: #ff4757;
        }

        .quiz-result-text {
            font-size: 1.2rem;
            color: #8892b0;
            margin-bottom: 30px;
        }

        /* User info */
        .user-info {
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(255,255,255,0.05);
            padding: 10px 20px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            gap: 15px;
            z-index: 100;
        }

        .user-role {
            color: #e94560;
            font-weight: 600;
        }

        .logout-btn {
            background: transparent;
            border: 1px solid rgba(255,255,255,0.2);
            color: #8892b0;
            padding: 5px 15px;
            border-radius: 5px;
            cursor: pointer;
            transition: all 0.3s;
        }

        .logout-btn:hover {
            border-color: #e94560;
            color: #e94560;
        }

        /* Progress bar in header */
        .progress-bar-container {
            margin-top: 20px;
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            height: 10px;
            overflow: hidden;
        }

        .progress-bar {
            height: 100%;
            background: linear-gradient(90deg, #e94560, #2ed573);
            border-radius: 10px;
            transition: width 0.5s ease;
        }

        .progress-text {
            margin-top: 10px;
            color: #8892b0;
            font-size: 0.9rem;
        }
'''

# Новый JavaScript
NEW_JS = '''
    <script src="quizzes.js"></script>
    <script>
        // ===== AUTH =====
        const ADMIN_PASSWORD = 'instinto2026';
        const STUDENT_PASSWORD = 'student2026';

        let currentUser = null;
        let progress = {};

        function initApp() {
            // Загружаем прогресс из localStorage
            const savedProgress = localStorage.getItem('academyProgress');
            if (savedProgress) {
                progress = JSON.parse(savedProgress);
            }

            // Проверяем авторизацию
            const savedUser = localStorage.getItem('academyUser');
            if (savedUser) {
                currentUser = JSON.parse(savedUser);
                showMainView();
            } else {
                showLoginScreen();
            }
        }

        function showLoginScreen() {
            document.getElementById('login-screen').classList.remove('hidden');
            document.getElementById('main-view').style.display = 'none';
        }

        function showMainView() {
            document.getElementById('login-screen').classList.add('hidden');
            document.getElementById('main-view').style.display = 'block';
            document.getElementById('user-info').style.display = 'flex';
            document.getElementById('user-role').textContent = currentUser.role === 'admin' ? 'Администратор' : 'Ученик';

            updateModulesAccess();
            updateProgressBar();
        }

        function login() {
            const password = document.getElementById('password-input').value;
            const errorEl = document.getElementById('login-error');

            if (password === ADMIN_PASSWORD) {
                currentUser = { role: 'admin' };
                localStorage.setItem('academyUser', JSON.stringify(currentUser));
                showMainView();
            } else if (password === STUDENT_PASSWORD) {
                currentUser = { role: 'student' };
                localStorage.setItem('academyUser', JSON.stringify(currentUser));
                showMainView();
            } else {
                errorEl.style.display = 'block';
                errorEl.textContent = 'Неверный пароль';
            }
        }

        function logout() {
            currentUser = null;
            localStorage.removeItem('academyUser');
            document.getElementById('user-info').style.display = 'none';
            showLoginScreen();
        }

        // ===== PROGRESS =====
        function saveProgress() {
            localStorage.setItem('academyProgress', JSON.stringify(progress));
        }

        function isModuleUnlocked(moduleNum) {
            if (currentUser && currentUser.role === 'admin') return true;
            if (moduleNum === 1) return true;
            return progress[moduleNum - 1] && progress[moduleNum - 1].passed;
        }

        function isModulePassed(moduleNum) {
            return progress[moduleNum] && progress[moduleNum].passed;
        }

        function updateModulesAccess() {
            const modules = document.querySelectorAll('.module[data-module]');
            modules.forEach(module => {
                const moduleNum = parseInt(module.dataset.module);
                const isUnlocked = isModuleUnlocked(moduleNum);
                const isPassed = isModulePassed(moduleNum);

                if (isUnlocked) {
                    module.classList.remove('locked');
                    const lockIcon = module.querySelector('.module-lock');
                    if (lockIcon) lockIcon.remove();
                } else {
                    module.classList.add('locked');
                    if (!module.querySelector('.module-lock')) {
                        const header = module.querySelector('.module-header');
                        const lock = document.createElement('div');
                        lock.className = 'module-lock';
                        lock.textContent = '🔒';
                        header.appendChild(lock);
                    }
                }

                // Обновляем бейдж
                const title = module.querySelector('.module-title');
                let badge = title.querySelector('.badge-progress, .badge-passed');
                if (badge) badge.remove();

                if (isPassed) {
                    const newBadge = document.createElement('span');
                    newBadge.className = 'badge badge-passed';
                    newBadge.textContent = '✓ Пройден';
                    title.appendChild(newBadge);
                } else if (isUnlocked && moduleNum > 1) {
                    const newBadge = document.createElement('span');
                    newBadge.className = 'badge badge-progress';
                    newBadge.textContent = 'Доступен';
                    title.appendChild(newBadge);
                }
            });
        }

        function updateProgressBar() {
            const totalModules = 14; // Модули с тестами
            let passedCount = 0;
            for (let i = 1; i <= totalModules; i++) {
                if (isModulePassed(i)) passedCount++;
            }

            const percent = Math.round((passedCount / totalModules) * 100);
            const bar = document.getElementById('progress-bar');
            const text = document.getElementById('progress-text');

            if (bar) bar.style.width = percent + '%';
            if (text) text.textContent = `Пройдено ${passedCount} из ${totalModules} модулей (${percent}%)`;
        }

        // ===== LESSONS =====
        function toggleModule(header) {
            const module = header.parentElement;
            if (module.classList.contains('locked')) return;
            module.classList.toggle('open');
        }

        let currentLessonId = null;

        function openLesson(lessonId) {
            const moduleNum = parseInt(lessonId.replace('lesson', ''));
            if (!isModuleUnlocked(moduleNum)) {
                alert('Сначала пройдите предыдущий модуль!');
                return;
            }

            currentLessonId = lessonId;
            const modal = document.getElementById('lessonModal');
            const content = document.getElementById('lessonContent');

            let lessonHTML = lessons[lessonId] || '<p>Урок ещё не готов</p>';

            // Добавляем кнопку теста в конце урока
            if (quizzes[moduleNum]) {
                lessonHTML += `
                    <div style="text-align: center; margin-top: 40px; padding-top: 30px; border-top: 2px solid rgba(233, 69, 96, 0.3);">
                        <button class="open-lesson-btn" onclick="startQuiz(${moduleNum})" style="margin: 0; font-size: 1.1rem; padding: 15px 40px;">
                            ${isModulePassed(moduleNum) ? '🔄 Пройти тест снова' : '📝 Пройти тест'}
                        </button>
                    </div>
                `;
            }

            content.innerHTML = lessonHTML;
            modal.classList.add('active');
            document.body.style.overflow = 'hidden';
        }

        function closeLesson() {
            const modal = document.getElementById('lessonModal');
            modal.classList.remove('active');
            document.body.style.overflow = '';
            currentLessonId = null;
        }

        // ===== QUIZ =====
        let currentQuiz = null;
        let currentQuestion = 0;
        let userAnswers = [];

        function startQuiz(moduleNum) {
            currentQuiz = quizzes[moduleNum];
            currentQuiz.moduleNum = moduleNum;
            currentQuestion = 0;
            userAnswers = new Array(currentQuiz.questions.length).fill(null);

            renderQuiz();
        }

        function renderQuiz() {
            const content = document.getElementById('lessonContent');
            const q = currentQuiz.questions[currentQuestion];

            let optionsHTML = q.options.map((opt, i) => `
                <div class="quiz-option ${userAnswers[currentQuestion] === i ? 'selected' : ''}"
                     onclick="selectAnswer(${i})">
                    ${String.fromCharCode(65 + i)}. ${opt}
                </div>
            `).join('');

            content.innerHTML = `
                <div class="quiz-container">
                    <div class="quiz-title">${currentQuiz.title}</div>
                    <div class="quiz-progress">Вопрос ${currentQuestion + 1} из ${currentQuiz.questions.length}</div>

                    <div class="quiz-question">
                        <div class="quiz-question-text">${q.q}</div>
                        <div class="quiz-options">
                            ${optionsHTML}
                        </div>
                    </div>

                    <div class="quiz-nav">
                        <button class="quiz-btn" onclick="prevQuestion()" ${currentQuestion === 0 ? 'style="visibility:hidden"' : ''}>
                            ← Назад
                        </button>
                        <button class="quiz-btn quiz-btn-next" onclick="nextQuestion()"
                                ${userAnswers[currentQuestion] === null ? 'disabled' : ''}>
                            ${currentQuestion === currentQuiz.questions.length - 1 ? 'Завершить' : 'Далее →'}
                        </button>
                    </div>
                </div>
            `;
        }

        function selectAnswer(index) {
            userAnswers[currentQuestion] = index;
            renderQuiz();
        }

        function prevQuestion() {
            if (currentQuestion > 0) {
                currentQuestion--;
                renderQuiz();
            }
        }

        function nextQuestion() {
            if (userAnswers[currentQuestion] === null) return;

            if (currentQuestion < currentQuiz.questions.length - 1) {
                currentQuestion++;
                renderQuiz();
            } else {
                showQuizResult();
            }
        }

        function showQuizResult() {
            let correct = 0;
            currentQuiz.questions.forEach((q, i) => {
                if (userAnswers[i] === q.correct) correct++;
            });

            const passed = correct >= 7;
            const moduleNum = currentQuiz.moduleNum;

            if (passed) {
                progress[moduleNum] = { passed: true, score: correct, date: new Date().toISOString() };
                saveProgress();
                updateModulesAccess();
                updateProgressBar();
            }

            const content = document.getElementById('lessonContent');
            content.innerHTML = `
                <div class="quiz-result">
                    <div class="quiz-result-score ${passed ? 'pass' : 'fail'}">${correct}/10</div>
                    <div class="quiz-result-text">
                        ${passed
                            ? '🎉 Отлично! Тест пройден. Следующий урок разблокирован!'
                            : '😕 Не хватило баллов. Нужно минимум 7/10. Перечитай урок и попробуй снова.'}
                    </div>
                    <button class="open-lesson-btn" onclick="${passed ? 'closeLesson()' : `openLesson('lesson${moduleNum}')`}" style="margin: 0;">
                        ${passed ? 'Вернуться к урокам' : 'Вернуться к уроку'}
                    </button>
                </div>
            `;
        }

        // ===== INIT =====
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') closeLesson();
            if (e.key === 'Enter' && document.getElementById('password-input') === document.activeElement) {
                login();
            }
        });

        document.addEventListener('DOMContentLoaded', initApp);
    </script>
'''

# HTML для экрана логина и user info
LOGIN_HTML = '''
    <!-- Login Screen -->
    <div class="login-screen" id="login-screen">
        <div class="login-box">
            <h2>Академия Instinto</h2>
            <p>Введите пароль для входа</p>
            <input type="password" class="login-input" id="password-input" placeholder="Пароль">
            <button class="login-btn" onclick="login()">Войти</button>
            <div class="login-error" id="login-error"></div>
        </div>
    </div>

    <!-- User Info -->
    <div class="user-info" id="user-info" style="display: none;">
        <span id="user-role" class="user-role"></span>
        <button class="logout-btn" onclick="logout()">Выйти</button>
    </div>
'''

# Прогресс бар для header
PROGRESS_BAR_HTML = '''
            <div class="progress-bar-container">
                <div class="progress-bar" id="progress-bar" style="width: 0%"></div>
            </div>
            <div class="progress-text" id="progress-text">Пройдено 0 из 14 модулей (0%)</div>
'''

def main():
    html = HTML_FILE.read_text(encoding='utf-8')

    # 1. Добавляем новые CSS стили перед </style>
    html = html.replace('    </style>', NEW_CSS + '    </style>')

    # 2. Добавляем login screen и user info после <body>
    html = html.replace('<body>', '<body>\n' + LOGIN_HTML)

    # 3. Добавляем прогресс бар после </div> в stats
    html = html.replace('</div>\n        </header>', '</div>' + PROGRESS_BAR_HTML + '\n        </header>')

    # 4. Добавляем data-module атрибуты к модулям
    for i in range(1, 18):
        old = f'<div class="module-number">{i}</div>'
        # Находим родительский div.module и добавляем data-module
        pattern = rf'(<div class="module[^"]*">)\s*(<div class="module-header"[^>]*>\s*<div class="module-number">{i}</div>)'
        replacement = rf'<div class="module" data-module="{i}">\n            <div class="module-header" onclick="toggleModule(this)">\n                <div class="module-number">{i}</div>'
        html = re.sub(pattern, replacement, html, count=1)

    # Убираем дублирующиеся классы
    html = re.sub(r'<div class="module" data-module="(\d+)">\s*<div class="module">',
                  r'<div class="module" data-module="\1">', html)

    # 5. Заменяем старый JavaScript на новый
    # Находим начало скрипта и заменяем всё до </script>
    script_start = html.find('<script>')
    script_end = html.find('</script>', script_start) + len('</script>')

    if script_start > 0 and script_end > script_start:
        old_script = html[script_start:script_end]
        # Сохраняем только объект lessons из старого скрипта
        lessons_match = re.search(r'(const lessons = \{[\s\S]*?\n        \};)', old_script)
        if lessons_match:
            lessons_obj = lessons_match.group(1)
            new_script = f'''<script>
        {lessons_obj}
    </script>
{NEW_JS}'''
            html = html[:script_start] + new_script + html[script_end:]

    HTML_FILE.write_text(html, encoding='utf-8')
    print("HTML обновлён с авторизацией и тестами")

if __name__ == '__main__':
    main()
