# hynix

SK하이닉스 AI 해커톤 2026 2차 예선용 개인 작업 키트.

## 들어 있는 것

`AGENTS.md` — 응시 환경 작업 규칙 (2차 예선 안내 PDF·운영팀 안내·Codex 공식 가이드 기준). 작업 폴더 루트에 두면 Codex가 자동으로 읽는다.

`skills/` — [mattpocock/skills](https://github.com/mattpocock/skills)(MIT, commit `59db609`)에서 고른 에이전트 스킬 9개. 원본 그대로이며 라이선스는 `LICENSE`.

| 단계 | 스킬 |
|---|---|
| 이해·질문 | `grill-me`, `grilling`, `to-questionnaire` |
| 작업 쪼개기 | `setup-matt-pocock-skills`, `to-tickets` |
| 구현·검증 | `tdd`, `code-review`, `diagnosing-bugs` |
| 인수인계 | `handoff` |

과제 결과물이나 과제별 코드는 넣지 않는다. 이 저장소는 2차 예선 결과 통지 전까지 공개 상태로 유지한다.

## 사용법 (작업 폴더에서)

아래 명령을 **과제 작업 폴더(README가 있는 곳)에서 그대로** 실행한다. 폴더 이름은 반드시 `.hynix`(점으로 시작)로 받고, 제출물에 섞이지 않게 git에서 제외한다.

```bash
git clone https://github.com/keepdev0919/hynix.git .hynix && echo ".hynix/" >> .git/info/exclude
mkdir -p .agents/skills && cp -R .hynix/skills/* .agents/skills/
if [ -f AGENTS.md ]; then cat .hynix/AGENTS.md >> AGENTS.md; else cp .hynix/AGENTS.md .; fi
```

- 과제 폴더에 이미 `AGENTS.md`가 있으면 덮어쓰지 않고 끝에 덧붙인다(위 세 번째 줄).
- 설치 후 확인: `ls .agents/skills`에 스킬 9개가 보이고, 새 Codex 세션의 `/skills` 목록에 나타나야 한다. 이미 열려 있던 Codex 세션은 다시 시작해야 스킬을 인식한다.

Codex에서 `$grill-me`, `$to-questionnaire`, `$to-tickets`, `$handoff` 처럼 이름으로 부른다.
