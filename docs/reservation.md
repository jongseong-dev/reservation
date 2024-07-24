# 예약 기능

## 개발 환경에서 초기 데이터 세팅

- 예약 신청을 할 수 있는 시험 일정을 생성한다.
- 로컬 환경 또는 테스트 환경에서만 사용할 수 있다.

```bash
python manage.py init_exam_schedule --settings=configs.settings.local
```

## 1. 예약 가능 일자 조회

- 사용자는 예약 가능 일자를 조회할 수 있다.
- 관리자도 접근 가능하다.

### Response

- `GET /api/v1/reservation/exam-schedule/`

```json
{
  "count": 123,
  "next": "...",
  "previous": "...",
  "results": [
    {
      "id": 0,
      "start_datetime": "2019-08-24T14:15:22+0000",
      "end_datetime": "2019-08-24T14:15:22+0000", 
      "remain_count": 0
    }
  ]
}
```

![img.png](img/exam_schedule_list_response.png)

- `GET /api/v1/reservation/exam-schedule/:id/`

```json
{
  "id": 1,
  "start_datetime": "2019-08-24T14:15:22+0000", 
  "end_datetime": "2019-08-24T14:15:22+0000",
  "remain_count": 0
}
```

![img.png](img/exam_schedule_detail_response.png)