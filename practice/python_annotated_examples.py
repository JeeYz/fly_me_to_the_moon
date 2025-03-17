"""
# Python의 typing.Annotated 사용 예제

이 파일은 Python의 typing 모듈에서 제공하는 Annotated 타입을 사용하는 다양한 예제를 포함하고 있습니다.
"""

# 예제 1: Annotated 기본 사용법
print("예제 1: Annotated 기본 사용법")
from typing import Annotated

# 기본 Annotated 사용 예
def example1():
    """
    Annotated의 기본 사용법을 보여주는 예제
    
    Annotated[타입, 메타데이터1, 메타데이터2, ...] 형식으로 사용합니다.
    메타데이터는 어떤 타입이든 될 수 있습니다.
    """
    # 메타데이터로 문자열 사용
    UserId = Annotated[int, "사용자 ID"]
    
    # 함수에서 Annotated 타입 사용
    def get_user(user_id: UserId) -> dict:
        """사용자 ID로 사용자 정보를 조회하는 함수"""
        return {"id": user_id, "name": f"사용자 {user_id}"}
    
    # 함수 호출
    user = get_user(123)
    print(f"사용자 정보: {user}")
    
    # 타입 정보 확인
    print(f"UserId의 타입: {UserId}")
    print(f"UserId의 __origin__: {UserId.__origin__}")
    print(f"UserId의 __metadata__: {UserId.__metadata__}")

example1()
print("\n" + "-"*50 + "\n")

# 예제 2: 여러 메타데이터 사용
print("예제 2: 여러 메타데이터 사용")
def example2():
    """
    Annotated에 여러 메타데이터를 사용하는 예제
    """
    # 여러 메타데이터 추가
    PositiveInt = Annotated[int, "양수", lambda x: x > 0]
    
    def validate_age(age: PositiveInt) -> None:
        """나이 유효성 검사 함수"""
        # 메타데이터에 포함된 검증 함수 사용
        validator = PositiveInt.__metadata__[1]
        if not validator(age):
            raise ValueError(f"나이는 양수여야 합니다. 입력값: {age}")
        print(f"유효한 나이: {age}")
    
    # 함수 호출
    try:
        validate_age(25)  # 정상 케이스
        validate_age(-5)  # 에러 케이스
    except ValueError as e:
        print(f"에러: {e}")

example2()
print("\n" + "-"*50 + "\n")

# 예제 3: 클래스와 함께 사용
print("예제 3: 클래스와 함께 사용")
from dataclasses import dataclass

def example3():
    """
    Annotated를 클래스와 함께 사용하는 예제
    """
    # 메타데이터로 클래스 사용
    class MaxLength:
        def __init__(self, max_length: int):
            self.max_length = max_length
        
        def validate(self, value: str) -> bool:
            return len(value) <= self.max_length
    
    # Annotated 타입 정의
    Username = Annotated[str, MaxLength(10)]
    Email = Annotated[str, "이메일 주소", lambda s: "@" in s]
    
    # 데이터클래스에서 사용
    @dataclass
    class User:
        username: Username
        email: Email
        
        def validate(self):
            # username 검증
            username_validator = Username.__metadata__[0]
            if not username_validator.validate(self.username):
                raise ValueError(f"사용자명은 {username_validator.max_length}자 이하여야 합니다.")
            
            # email 검증
            email_validator = Email.__metadata__[1]
            if not email_validator(self.email):
                raise ValueError("이메일 주소는 @ 기호를 포함해야 합니다.")
            
            return True
    
    # 사용 예
    try:
        # 유효한 사용자
        user1 = User(username="user123", email="user@example.com")
        user1.validate()
        print(f"유효한 사용자: {user1}")
        
        # 유효하지 않은 사용자명 (길이 초과)
        user2 = User(username="very_long_username", email="user@example.com")
        user2.validate()
    except ValueError as e:
        print(f"에러: {e}")
    
    try:
        # 유효하지 않은 이메일 (@ 없음)
        user3 = User(username="user123", email="invalid_email")
        user3.validate()
    except ValueError as e:
        print(f"에러: {e}")

example3()
print("\n" + "-"*50 + "\n")

# 예제 4: 의존성 주입 시뮬레이션
print("예제 4: 의존성 주입 시뮬레이션")
def example4():
    """
    Annotated를 사용한 의존성 주입 시뮬레이션 예제
    (FastAPI나 다른 프레임워크에서 사용하는 방식과 유사)
    """
    # 의존성 클래스
    class Dependency:
        def __init__(self, name: str):
            self.name = name
        
        def __call__(self):
            return f"{self.name} 의존성 제공"
    
    # 의존성 정의
    DatabaseDep = Annotated[dict, Dependency("데이터베이스")]
    LoggerDep = Annotated[object, Dependency("로거")]
    
    # 의존성 주입 시뮬레이션 함수
    def inject_dependencies(func):
        """함수의 매개변수에 의존성을 주입하는 데코레이터"""
        def wrapper(*args, **kwargs):
            # 함수 어노테이션 확인
            for param_name, param_type in func.__annotations__.items():
                if hasattr(param_type, '__metadata__'):
                    for meta in param_type.__metadata__:
                        if isinstance(meta, Dependency):
                            # 의존성 주입
                            kwargs[param_name] = meta()
            return func(*args, **kwargs)
        return wrapper
    
    # 의존성 주입을 사용하는 함수
    @inject_dependencies
    def process_data(db: DatabaseDep, logger: LoggerDep) -> str:
        """데이터 처리 함수"""
        return f"데이터 처리 중: {db}, {logger}"
    
    # 함수 호출
    result = process_data()
    print(f"결과: {result}")

example4()
print("\n" + "-"*50 + "\n")


# 유효성 검사기 클래스들
class Validator:
    """기본 유효성 검사기 클래스"""
    def validate(self, value):
        raise NotImplementedError()
    

class MinLength(Validator):
    def __init__(self, min_length: int):
        self.min_length = min_length
    
    def validate(self, value):
        if len(value) < self.min_length:
            raise ValueError(f"값의 길이는 최소 {self.min_length}여야 합니다.")
        return value

class Pattern(Validator):
    def __init__(self, pattern: str):
        self.pattern = pattern
    
    def validate(self, value):
        import re
        if not re.match(self.pattern, value):
            raise ValueError(f"값은 패턴 '{self.pattern}'과 일치해야 합니다.")
        return value
    
# 예제 5: 실제 유효성 검사 라이브러리 시뮬레이션
print("예제 5: 실제 유효성 검사 라이브러리 시뮬레이션")
def example5():
    """
    Pydantic과 유사한 유효성 검사 라이브러리를 시뮬레이션하는 예제
    """
    # 유효성 검사 함수
    def validate_field(field_name: str, value, annotated_type):
        """필드 유효성 검사 함수"""
        if not hasattr(annotated_type, '__metadata__'):
            return value
        
        # 모든 유효성 검사기 실행
        for meta in annotated_type.__metadata__:
            if isinstance(meta, Validator):
                try:
                    value = meta.validate(value)
                except ValueError as e:
                    raise ValueError(f"필드 '{field_name}' 유효성 검사 실패: {e}")
        
        return value
    
    # Annotated 타입 정의
    Password = Annotated[str, MinLength(8), Pattern(r'.*[A-Z].*')]
    
    # 사용 예
    try:
        # 유효한 비밀번호
        valid_password = "SecurePass123"
        validated = validate_field("password", valid_password, Password)
        print(f"유효한 비밀번호: {validated}")
        
        # 유효하지 않은 비밀번호 (길이 부족)
        invalid_password1 = "short"
        validate_field("password", invalid_password1, Password)
    except ValueError as e:
        print(f"에러: {e}")
    
    try:
        # 유효하지 않은 비밀번호 (대문자 없음)
        invalid_password2 = "nouppercase123"
        validate_field("password", invalid_password2, Password)
    except ValueError as e:
        print(f"에러: {e}")

example5()
print("\n" + "-"*50 + "\n")

# 예제 6: 타입 힌트 도구와의 통합
print("예제 6: 타입 힌트 도구와의 통합")
def example6():
    """
    mypy나 다른 타입 검사 도구와 Annotated 통합 예제
    """
    # 타입 체커는 Annotated의 첫 번째 인자만 고려함
    Vector = Annotated[list[float], "2D 벡터"]
    
    def calculate_magnitude(vector: Vector) -> float:
        """벡터의 크기를 계산하는 함수"""
        return sum(x**2 for x in vector) ** 0.5
    
    # 사용 예
    v = [3.0, 4.0]
    magnitude = calculate_magnitude(v)
    print(f"벡터 {v}의 크기: {magnitude}")
    
    # 타입 힌트 주석
    print("이 예제는 mypy와 같은 타입 체커에서 Vector가 list[float]로 인식됨을 보여줍니다.")
    print("타입 체커는 메타데이터('2D 벡터')를 무시하고 타입 검사만 수행합니다.")

example6()
print("\n" + "-"*50 + "\n")

# 예제 7: 복잡한 중첩 타입
print("예제 7: 복잡한 중첩 타입")
from typing import Dict, List, Optional, Union

def example7():
    """
    복잡한 중첩 타입에서 Annotated 사용 예제
    """
    # 복잡한 중첩 타입 정의
    UserId = Annotated[int, "사용자 고유 ID"]
    UserName = Annotated[str, "사용자 이름", MinLength(3)]
    UserData = Dict[UserId, UserName]
    
    ComplexType = Annotated[
        List[Union[UserData, Optional[Dict[str, int]]]],
        "복잡한 사용자 데이터 구조"
    ]
    
    # 사용 예
    def process_complex_data(data: ComplexType) -> str:
        """복잡한 데이터 처리 함수"""
        return f"복잡한 데이터 처리 완료: {len(data)} 항목"
    
    # 샘플 데이터
    sample_data = [
        {123: "user123"},  # UserData
        {"score": 95, "rank": 1},  # Dict[str, int]
        None,  # Optional
    ]
    
    result = process_complex_data(sample_data)
    print(f"결과: {result}")
    print(f"ComplexType.__origin__: {ComplexType.__origin__}")
    print(f"ComplexType.__metadata__: {ComplexType.__metadata__}")

example7()
print("\n" + "-"*50 + "\n")

print("모든 예제 실행 완료!")
"""
이 예제들은 Python의 typing.Annotated를 다양한 상황에서 활용하는 방법을 보여줍니다.
실제 프로젝트에서는 FastAPI, Pydantic 등의 라이브러리에서 Annotated를 활용하여
의존성 주입, 유효성 검사 등 다양한 기능을 구현할 수 있습니다.
"""
