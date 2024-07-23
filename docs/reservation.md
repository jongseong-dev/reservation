# 예약 기능

## 1. 예약된 일자 조회 API

- 사용자는 해당 API를 통해 예약된 일자를 조회할 수 있습니다.
- 관리자도 접근 가능합니다.

### Request 

- Method: GET
- URL: /api/reservation/
- Query Params
  - start_datetime: 예약 일자 조회 시작일자 (YYYY-MM-DD)
  - end_datetime: 예약 일자 조회 종료일자 (YYYY-MM-DD)
  - available: 예약 가능 여부 (True/False)
    - True: 예약 되었지만 가능한 일자만 조회
    - False: 예약이 불가능 일자만 조회
- Response
    - description: 예약된 시간 조회
    - status: 200
        - items: object
            - reserved_datetime: 예약된 날짜
            - reserved_count: 예약된 인원 수
            - available: 예약 가능 여부
    - status: 401
        - description: 인증되지 않은 사용자