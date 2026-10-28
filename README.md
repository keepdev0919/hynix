# hynix

SK하이닉스 AI 해커톤 2026 2차 예선용 개인 작업 키트.

## 들어 있는 것

`skills/` — [mattpocock/skills](https://github.com/mattpocock/skills)(MIT, commit `59db609`)에서 고른 에이전트 스킬 9개. 원본 그대로이며 라이선스는 `LICENSE`.

| 단계 | 스킬 |
|---|---|
| 이해·질문 | `grill-me`, `grilling`, `to-questionnaire` |
| 작업 쪼개기 | `setup-matt-pocock-skills`, `to-tickets` |
| 구현·검증 | `tdd`, `code-review`, `diagnosing-bugs` |
| 인수인계 | `handoff` |

과제 결과물이나 과제별 코드는 넣지 않는다. 이 저장소는 2차 예선 결과 통지 전까지 공개 상태로 유지한다.

## 사용법 (작업 폴더에서)

```bash
git clone https://github.com/keepdev0919/hynix.git .hynix
mkdir -p .agents/skills && cp -R .hynix/skills/* .agents/skills/
```

Codex에서 `$grill-me`, `$to-questionnaire`, `$to-tickets`, `$handoff` 처럼 이름으로 부른다.
