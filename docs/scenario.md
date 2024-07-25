# 사용자 시나리오

## 전제 조건
- 이 시스템은 로그인이 필요한 서비스이다.
- 관리자 계정은 미리 생성 되어 있다.
- 일반 고객은 회원가입을 통해 가입한다.

## 회원가입 & 로그인하기

- 기업 고객은 시험 시스템을 이용하고자 한다.
- 고객은 시스템에 가입한다.
    - `POST /api/account/signup/`을 통해 시스템에 가입한다.
- 가입한 고객은 로그인을 한다.
    - `POST /api/token/`을 통해 로그인한다
    - 인증 방식은 `jwt`로 한다.
      - why?
        - claim 에 필요한 정보를 넣을 수 있어 확장성이 좋고 token 기반 인증이기 때문에 stateless한 rest api 인증방식에 어울린다고 판단.

## 예약 가능한 시험 일정 조회하기

- 시험 예약을 할 수 있는 시간대를 조회한다.
    - `GET /api/v1/reservation/exam-schedule/`을 통해 시험 예약 가능한 시간대를 조회한다.
    - 현재 2시간 단위로 예약이 가능하다
    - 예약 가능한 시간대는 3일 전까지만 조회 가능하다.
    - 예약 가능한 시간대는 최대 5만명까지 예약 가능하다.
    - filter와 ordering 기능을 제공한다. 해당 기능에 대한 상세한 설명은 api docs를 참고할 것
- 예약 시간대의 상세한 조회를 하고자 한다
    - `GET /api/v1/reservation/exam-schedule/:exam_schedule_id`을 통해 상세 조회 가능

## 시험 예약하기

- 해당 시험 일정을 조회했다면 시험을 신청하고자 한다.
  - `POST /api/v1/reservation/`을 통해 시험을 신청한다.
  - 시험 예약에는 시험 일정 정보를 담고있는 exam_schedule_id와 응시 인원을 담고있는 reserved_count가 필요하다.
  - 시험 예약은 최대 5만명까지 가능하다.
  - 단 관리자가 확정하기 전까지는 예약 인원에 포함되지 않는다.
  - 시험 일정은 3일 전까지만 예약 가능하다.

## 시험 확정하기

- 관리자는 시험을 확정할 수 있다.
  - `POST /api/v1/reservation/:reservation_id/reserved/`을 통해 시험을 확정한다.
  - 확정된 시험은 예약 인원에 포함된다.
  - 확정된 시험은 취소할 수 없다.

## 시험 취소하기

- 관리자는 확정되지 않은 시험을 삭제할 수 있다.
  - `DELETE /api/v1/reservation/:reservation_id/canceled`을 통해 시험을 삭제한다.
  - soft delete 이므로 관리자가 조회하는 예약 조회에서는 보일 수 있다.

- 고객은 본인의 시험을 삭제할 수 있다.
  - `DELETE /api/v1/reservation/:reservation_id/canceled`을 통해 시험을 삭제한다. 
  - 확정된 시험은 삭제할 수 없다.
  - soft delete 이지만 삭제한 내역은 조회할 수 없다

## 시험 수정하기

- 관리자는 모든 고객의 시험을 수정할 수 있다.
  - `PUT /admin/api/v1/reservation/:reservation_id/`을 통해 시험을 수정한다.
  - 확정된 시험은 수정할 수 없다.

- 고객은 본인의 시험을 수정할 수 있다.
  - `PUT /api/v1/reservation/:reservation_id/`을 통해 시험을 수정한다.
  - 확정된 시험은 수정할 수 없다.