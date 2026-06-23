# Decision Framework

Use this framework before creating or updating a progress cockpit.

## 1. Decide Whether A Progress Screen Is Needed

Create or update it when:

- the project has several phases or skills;
- the user is non-technical and needs plain-language visibility;
- the workflow has user choices, comments, approvals, or missing data gates;
- the project spans multiple sessions;
- the user explicitly asks to see how the agent system works.

Create a bootstrap screen immediately when:

- `senior-ui-ux-orchestrator` accepts a substantial UI/UX project request;
- `TASK-PLAN.md` does not exist yet;
- planning, research, design, Stitch, Figma, code, or external checks may take more than a trivial moment;
- the user needs to see that the system accepted the request and is forming the plan.

Skip or offer it as optional when:

- the task is a tiny one-file edit;
- there is no task plan yet;
- the page would expose private data that cannot be sanitized.

## 2. Choose Update Mode

Prefer bootstrap first, then static regeneration:

```text
project-request.json + workflow-log.jsonl
-> bootstrap progress-state.json
-> bootstrap agent-progress-screen.html
-> open browser
```

After the task plan exists:

```text
TASK-PLAN.md -> progress-state.json -> agent-progress-screen.html
```

Use live refresh only when a local server is available and the user wants automatic browser updates. Static `file://` mode must remain valid.

## 3. Choose Copy Mode

Default customer mode:

- plain human language;
- visible next action;
- phase/subprocess status;
- artifact links;
- comments and choices.

Developer mode:

- task ids;
- skill routes;
- dependency lists;
- source artifacts;
- validation reports.

## 4. Decide User Gates

Show a user gate only when the system genuinely waits for the user:

- design direction choice;
- content/fact approval;
- missing contact/domain/project data;
- final review;
- launch confirmation.

Do not create fake waiting states for tasks that are merely planned. Bootstrap may show "forming plan" as running only until `TASK-PLAN.md` is created.

## 5. Decide Feedback Persistence

If the page cannot write to disk, the UI may help the user copy a structured feedback payload. The actual durable record must be saved into a feedback artifact or task-plan/wiki decision by the agent.
