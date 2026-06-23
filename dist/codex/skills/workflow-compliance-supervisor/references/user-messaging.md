# User Messaging

Use plain language. Do not expose internal skill names unless the user asks for developer details.

## pause_for_user

Message: "Нужны ваши данные или разрешение, иначе система может сделать неправильный шаг."

Options:
- provide missing data;
- approve the external or production action;
- continue local-only;
- change scope.

## return_to_rework

Message: "Этап заявлен как готовый, но доказательств недостаточно. Возвращаем на доработку."

Options:
- rerun the missing check;
- create a repair task;
- accept a manual check if the task allows it.

## skip_with_reason

Message: "Этап пропущен осознанно. Причина и влияние зафиксированы."

Options:
- accept skip;
- request execution;
- create follow-up task.

## block

Message: "Дальше идти нельзя без риска для качества, приватности или запуска."

Options:
- provide missing approval/data;
- reduce scope;
- stop and repair.

