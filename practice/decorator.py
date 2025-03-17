# Python 데코레이터 예제 모음

import time
import functools
from typing import Callable, Any, TypeVar, cast
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)



# 예제 1: 기본 함수 데코레이터
def simple_decorator(func):
    """함수 실행 전후에 메시지를 출력하는 간단한 데코레이터"""
    
    @functools.wraps(func)  # 원본 함수의 메타데이터 보존
    def wrapper(*args, **kwargs):
        print(f"함수 {func.__name__} 실행 전")
        func(*args, **kwargs)
        print(f"함수 {func.__name__} 실행 후")
        # return result
    
    return wrapper


@simple_decorator
def say_hello(name):
    """인사말을 출력하는 함수"""
    print(f"안녕하세요, {name}님!")



# 예제 2: 매개변수가 있는 데코레이터
def repeat(n=2):
    """함수를 n번 반복 실행하는 데코레이터"""
    
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(n):
                results.append(func(*args, **kwargs))
            return results
        return wrapper
    
    return decorator


@repeat(n=3)
def greet(name):
    """인사말을 반환하는 함수"""
    return f"안녕하세요, {name}님!"


# 예제 3: 실행 시간 측정 데코레이터
def timer(func):
    """함수의 실행 시간을 측정하는 데코레이터"""
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} 함수 실행 시간: {end_time - start_time:.4f}초")
        return result
    
    return wrapper


@timer
def slow_function():
    """시간이 오래 걸리는 함수 시뮬레이션"""
    time.sleep(1)
    return "완료"


# 예제 4: 로깅 데코레이터
def log_function_call(func):
    """함수 호출을 로깅하는 데코레이터"""
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        
        logger.info(f"함수 {func.__name__}({signature}) 호출됨")
        try:
            result = func(*args, **kwargs)
            logger.info(f"함수 {func.__name__} 결과: {result!r}")
            return result
        except Exception as e:
            logger.exception(f"함수 {func.__name__} 예외 발생: {e}")
            raise
    
    return wrapper



@log_function_call
def divide(a, b):
    """두 숫자를 나누는 함수"""
    return a / b


# 예제 5: 캐싱 데코레이터 (메모이제이션)
def memoize(func):
    """함수 호출 결과를 캐싱하는 데코레이터"""
    cache = {}
    
    @functools.wraps(func)
    def wrapper(*args):
        if args in cache:
            print(f"캐시에서 결과 가져옴: {args}")
            return cache[args]
        
        result = func(*args)
        cache[args] = result
        print(f"결과 계산 및 캐싱: {args} -> {result}")
        return result
    
    return wrapper


@memoize
def fibonacci(n):
    """피보나치 수열의 n번째 값을 계산하는 함수"""
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)


# 예제 6: 접근 제어 데코레이터
def require_auth(func):
    """인증이 필요한 함수에 대한 데코레이터"""
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 실제로는 세션이나 토큰을 확인해야 함
        is_authenticated = kwargs.pop('is_authenticated', False)
        
        if is_authenticated:
            return func(*args, **kwargs)
        else:
            return "인증이 필요합니다."
    
    return wrapper


@require_auth
def get_secret_data():
    """비밀 데이터를 반환하는 함수"""
    return "이것은 비밀 데이터입니다."


# 예제 7: 재시도 데코레이터
def retry(max_attempts=3, delay=1):
    """지정된 횟수만큼 함수 실행을 재시도하는 데코레이터"""
    
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise
                    print(f"오류 발생: {e}. {delay}초 후 재시도... (시도 {attempts}/{max_attempts})")
                    time.sleep(delay)
        return wrapper
    
    return decorator


@retry(max_attempts=3, delay=0.5)
def unstable_function():
    """가끔 실패하는 불안정한 함수 시뮬레이션"""
    import random
    if random.random() < 0.7:  # 70% 확률로 실패
        raise ValueError("무작위 오류 발생")
    return "성공!"


# 예제 8: 타입 검사 데코레이터
T = TypeVar('T')

def type_check(func: Callable[..., T]) -> Callable[..., T]:
    """함수 인자의 타입을 검사하는 데코레이터"""
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        hints = func.__annotations__
        
        # 위치 인자 검사
        for arg, arg_type in zip(args, [hints[param] for param in list(hints.keys())[:-1]]):
            if not isinstance(arg, arg_type):
                raise TypeError(f"인자 {arg}의 타입이 {type(arg)}이지만, {arg_type}이 필요합니다.")
        
        # 키워드 인자 검사 (간단한 구현)
        for param_name, arg in kwargs.items():
            if param_name in hints and not isinstance(arg, hints[param_name]):
                raise TypeError(f"인자 {param_name}={arg}의 타입이 {type(arg)}이지만, {hints[param_name]}이 필요합니다.")
        
        result = func(*args, **kwargs)
        
        # 반환값 검사
        if 'return' in hints and not isinstance(result, hints['return']):
            raise TypeError(f"반환값 {result}의 타입이 {type(result)}이지만, {hints['return']}이 필요합니다.")
        
        return result
    
    return wrapper


@type_check
def add_numbers(a: int, b: int) -> int:
    """두 정수를 더하는 함수"""
    return a + b


# 예제 9: 클래스 데코레이터
def singleton(cls):
    """클래스를 싱글톤으로 만드는 데코레이터"""
    instances = {}
    
    @functools.wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance


@singleton
class DatabaseConnection:
    """데이터베이스 연결을 관리하는 싱글톤 클래스"""
    
    def __init__(self, host="localhost"):
        self.host = host
        self.connected = False
        print(f"데이터베이스 연결 객체 생성: {host}")
    
    def connect(self):
        if not self.connected:
            print(f"{self.host}에 연결 중...")
            self.connected = True
            return True
        return False


# 예제 10: 메서드 데코레이터
def validate_arguments(method):
    """메서드 인자를 검증하는 데코레이터"""
    
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        # self는 클래스 인스턴스
        for arg in args:
            if arg < 0:
                raise ValueError("음수 값은 허용되지 않습니다.")
        
        for _, value in kwargs.items():
            if isinstance(value, (int, float)) and value < 0:
                raise ValueError("음수 값은 허용되지 않습니다.")
        
        return method(self, *args, **kwargs)
    
    return wrapper


class Calculator:
    """간단한 계산기 클래스"""
    
    @validate_arguments
    def add(self, a, b):
        """두 수를 더하는 메서드"""
        return a + b
    
    @validate_arguments
    def subtract(self, a, b):
        """두 수를 빼는 메서드"""
        return a - b


# 메인 실행 코드
if __name__ == "__main__":
    print("\n=== 예제 1: 기본 함수 데코레이터 ===")
    say_hello("홍길동")
    
    print("\n=== 예제 2: 매개변수가 있는 데코레이터 ===")
    results = greet("김철수")
    for result in results:
        print(result)
    
    print("\n=== 예제 3: 실행 시간 측정 데코레이터 ===")
    slow_function()
    
    print("\n=== 예제 4: 로깅 데코레이터 ===")
    divide(10, 2)
    try:
        divide(10, 0)
    except ZeroDivisionError:
        print("0으로 나눌 수 없습니다.")
    
    print("\n=== 예제 5: 캐싱 데코레이터 ===")
    print(f"fibonacci(6) = {fibonacci(6)}")
    print(f"fibonacci(6) 다시 호출 = {fibonacci(6)}")
    
    print("\n=== 예제 6: 접근 제어 데코레이터 ===")
    print(get_secret_data())  # 인증 없음
    print(get_secret_data(is_authenticated=True))  # 인증 있음
    
    print("\n=== 예제 7: 재시도 데코레이터 ===")
    try:
        result = unstable_function()
        print(f"결과: {result}")
    except ValueError as e:
        print(f"최종 오류: {e}")
    
    print("\n=== 예제 8: 타입 검사 데코레이터 ===")
    print(f"add_numbers(3, 5) = {add_numbers(3, 5)}")
    try:
        add_numbers(3, "5")
    except TypeError as e:
        print(f"타입 오류: {e}")
    
    print("\n=== 예제 9: 클래스 데코레이터 ===")
    db1 = DatabaseConnection()
    db2 = DatabaseConnection("127.0.0.1")
    print(f"db1과 db2는 같은 객체인가? {db1 is db2}")
    db1.connect()
    db2.connect()  # 이미 연결됨
    
    print("\n=== 예제 10: 메서드 데코레이터 ===")
    calc = Calculator()
    print(f"calc.add(10, 20) = {calc.add(10, 20)}")
    try:
        calc.subtract(10, -5)
    except ValueError as e:
        print(f"검증 오류: {e}")