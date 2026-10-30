---
name: situation-brief
description: 과제 README와 데이터 파일을 읽고, 상황 설명·데이터 사전·검증 차트·원본 표가 있는 브리핑 화면을 만든다. 과제 시작 직후 또는 "상황 이해가 안 돼", "데이터를 어떻게 봐야 해"라고 할 때 쓴다.
---

사용자가 도메인과 데이터를 이해하도록 돕는다. 무엇을 만들지는 제안하지 않는다. 아직 실무자에게 듣지 못한 내용은 추측하지 말고 "미확인"으로 쓴다.

이 스킬은 이해를 돕는 단계이지 구현이 아니다. `.brief/` 밖에 파일을 만들지 않고, 테스트·메모·결정 기록·SOLUTION·결과 요약을 쓰지 않으며, 커밋하지 않는다. 데이터를 다시 분석하지 말고 짧게 끝낸다.

숫자는 스크립트가 계산한다. 네가 직접 계산한 숫자를 화면에 적지 않는다. 필요한 숫자는 `views`로 계산하게 한다.

## 순서

1. 과제 README와 안내 문서를 읽고, 스크립트로 데이터를 요약한다. 데이터 폴더가 다르면 `--data`로 지정한다.
   ```bash
   python3 .agents/skills/situation-brief/scripts/build_brief.py profile --data data
   ```
   결과는 `.brief/profile.json`이다. 큰 파일을 통째로 읽지 말고 이 결과를 본다.
2. `.brief/brief.json`을 아래 형식으로 쓴다. 쉬운 말로, 전문 용어는 `terms`에 풀어 쓴다.
3. 화면을 만들고 띄운다.
   ```bash
   python3 .agents/skills/situation-brief/scripts/build_brief.py build --data data
   python3 -m http.server 4000 --bind 0.0.0.0 --directory .brief
   ```
4. 사용자에게 "Browser에서 PORT 4000, 경로 /" 라고 알린다. 다 봤으면 이 서버를 끈다. 서비스 서버와 메모리를 같이 쓰기 때문이다.

`.brief/`는 작업 도구이며 제출물이 아니다. 여기서 얻은 판단은 메모에 옮겨 적는다.

## brief.json 형식

```json
{
  "summary": "이 상황을 중학생에게 설명하는 세 문장",
  "analogy": "일상 비유 하나",
  "people": [{"who": "누가", "does": "무엇을 하고", "pain": "무엇이 힘든가"}],
  "flow": ["지금 일이 흘러가는 순서 한 단계씩"],
  "terms": [{"term": "용어", "meaning": "쉬운 뜻"}],
  "files": [{"file": "파일명", "row_means": "한 줄이 뜻하는 것", "columns": {"컬럼": "뜻"}, "use": "무엇을 알 수 있나"}],
  "stories": [{"quote": "README에 나온 현장 이야기", "check": "데이터로 확인할 것", "view": "views의 title 또는 빈 값(데이터로 못 봄)"}],
  "views": [{
    "title": "차트 제목",
    "question": "이 차트가 답하는 질문",
    "file": "파일명",
    "group_by": ["컬럼"],
    "agg": "count|sum|mean|ratio|rate",
    "value": "숫자 컬럼 (sum·mean·ratio)",
    "over": "분모 컬럼 (ratio)",
    "when": {"left": "컬럼", "op": ">=|<=|==|!=|>|<", "right": "컬럼 또는 값"},
    "filter": {"컬럼": "값"},
    "reading": "차트 읽는 법 한 줄. 숫자를 쓰지 않는다."
  }],
  "cautions": ["profile에서 본 이상 신호와 왜 조심해야 하는지"],
  "ask": ["데이터만으로 모르는 것, 실무자에게 물을 사실 질문"],
  "cases": []
}
```

- `group_by` 항목에는 `날짜컬럼:weekday`, `날짜컬럼:week`, `날짜컬럼:month`도 쓸 수 있다. 첫 항목이 가로축, 둘째 항목이 묶음 기준이다.
- `rate`는 `when` 조건을 만족하는 줄의 비율이다. `ratio`는 `value` 합 ÷ `over` 합이다.
- 차트는 4~7개. `stories`의 현장 이야기를 확인하는 차트를 먼저 만든다.
- `profile.json`의 `signals`는 `cautions`에 반드시 반영한다. 특히 `ceiling`(값이 다른 컬럼에서 멈춤)은 진짜 수요가 안 보인다는 뜻일 수 있다.
