# FEATURE-PREPARATION

feature_id:
feature_title:
status: draft
owner_role: planner
last_updated:

## 1. Problem and goal
- [ ] Фича названа одним ясным предложением
- [ ] Понятно, какую проблему она решает
- [ ] Определен основной пользователь
- [ ] Определена ценность фичи
- [ ] Понятно, что не входит в фичу

## 2. User intents
- [ ] Собраны 5-10 типовых пользовательских команд
- [ ] Описаны основные user flows
- [ ] Описаны неоднозначные запросы
- [ ] Описаны ошибки и edge cases
- [ ] Определено, когда AI должен уточнять запрос

## 3. UI/UX
- [ ] Определено, где пользователь вызывает фичу
- [ ] Определен основной UI-паттерн: чат, command bar, panel, modal
- [ ] Понятно, как выглядит preview результата
- [ ] Понятно, как подтвердить применение
- [ ] Понятно, как сделать undo/rollback
- [ ] Описаны состояния UI
- [ ] Описано поведение при ошибке или низкой уверенности

## 4. Technical design
- [ ] Определены затрагиваемые подсистемы
- [ ] Определена точка входа AI layer
- [ ] Описан путь intent -> internal action
- [ ] Понятно, какие API/events/contracts нужны
- [ ] Определены ограничения и forbidden areas
- [ ] Решено, нужен ли preview/dry-run mode
- [ ] Если предлагаются mock/stub/placeholder элементы, на них заведены alarms с условиями замены

## 5. Verification
- [ ] Для фичи есть acceptance criteria
- [ ] Для каждого ключевого сценария есть способ проверки
- [ ] Определены unit/integration/e2e тесты
- [ ] Подготовлены fixtures или sample data
- [ ] Определен oracle успеха
- [ ] Определены negative tests
- [ ] Определены regression risks
- [ ] Понятно, чего именно не хватает, чтобы заменить каждый временный mock/placeholder

## 6. Delivery and rollout
- [ ] Определен MVP-срез
- [ ] Определено, что отложено на потом
- [ ] Решено, нужен ли feature flag
- [ ] Определен rollback/fallback
- [ ] Определено, что писать в wiki
- [ ] Определено, какие артефакты должен вернуть Codex

## Decisions

problem_statement:
primary_user:
value:
mvp_slice:
deferred_scope:
feature_flag:
rollback:
required_artifacts:
wiki_updates:
