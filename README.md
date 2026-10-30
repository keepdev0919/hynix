# hynix

SK하이닉스 AI 해커톤 2026 2차 예선용 개인 작업 키트.

## 들어 있는 것

`AGENTS.md` — 응시 환경 작업 규칙 (2차 예선 안내 PDF·운영팀 안내·Codex 공식 가이드 기준). 작업 폴더 루트에 두면 Codex가 자동으로 읽는다.

`CONTEXT.md` — 시험 구조·평가 기준·응시 환경·작업 흐름 배경지식. Codex가 작업 전에 읽는다.

과제 결과물이나 과제별 코드는 넣지 않는다. 이 저장소는 2차 예선 결과 통지 전까지 공개 상태로 유지한다.

## 사용법 (작업 폴더에서)

아래 명령을 **과제 작업 폴더(README가 있는 곳)에서 그대로** 실행한다. 폴더 이름은 반드시 `.hynix`(점으로 시작)로 받고, 제출물에 섞이지 않게 git에서 제외한다.

```bash
git clone https://github.com/keepdev0919/hynix.git .hynix && echo ".hynix/" >> .git/info/exclude
if [ -f AGENTS.md ]; then cat .hynix/AGENTS.md >> AGENTS.md; else cp .hynix/AGENTS.md .; fi
```

- 과제 폴더에 이미 `AGENTS.md`가 있으면 덮어쓰지 않고 끝에 덧붙인다(위 두 번째 줄).
- 이미 열려 있던 Codex 세션은 다시 시작해야 규칙을 읽는다.

## Codex 실행 옵션 (승인 창 줄이기)

사전체험에서는 Codex가 서버를 켤 때마다 승인 창이 떴다. 샌드박스(Codex의 작업 울타리)가 서버 소켓 생성을 막았기 때문이다. 아래 명령은 **사용자가** Codex를 끄고(`/quit`) 다시 켤 때 쓴다.

```bash
codex -s workspace-write -a never -c sandbox_workspace_write.network_access=true
```

① 기본: 작업 폴더 안 수정과 네트워크(서버 켜기 포함)는 묻지 않고 하고, 울타리 밖 작업은 묻지 않고 실패로 보고한다. 울타리는 그대로 둔다.

```bash
codex --dangerously-bypass-approvals-and-sandbox
```

② 비상용: 승인과 울타리를 모두 끈다. ①로 서버가 뜨지 않을 때만 쓰고, 썼다면 결정 기록에 이유를 한 줄 남긴다.

쓰기 전에:
- 실제 응시 환경 메신저에는 Cofa Helper가 없고 과제 담당자만 있다. 담당자는 업무 배경만 답하므로 이 설정을 묻지 않는다.
- 그래서 아래 Codex 확인 결과와 시험 안내 문구로 판단한다. 걸리는 게 없으면 ①로 가고, 하나라도 걸리면 기본 설정 그대로 간다.
- 실제 응시 환경에서 ①·② 모두 미확인이다(로컬 Codex 0.165 기준으로 작성, 응시 환경은 0.163).

> **Codex에게:** 이 절은 사용자용이다. 너는 이 명령을 직접 실행하거나 Codex를 재시작하지 않는다. 키트를 설치한 뒤 아래를 확인해서 결과만 짧게 알려 준다.
> - `codex --help`에 `-s`, `-a`, `--dangerously-bypass-approvals-and-sandbox` 옵션이 있는가.
> - 플랫폼이 승인·샌드박스를 고정해 둔 설정이 있는가(`~/.codex/config.toml`, `/etc/codex/` 등). 읽기만 하고 고치지 않는다.
> - 시험 안내·README·과제 지침에 이 설정과 부딪치는 문장이 있는가.
>
> 하나라도 걸리면 "이 환경에서는 ①/②를 쓰지 않는 게 좋겠다"와 그 이유를 말한다. ②를 쓸지는 사용자가 정한다.
