class InsufficientBalanceException(Exception):
    pass

class TimeoutException(Exception):
    pass

class CallNotPermittedException(Exception):
    pass

class CircuitBreaker:
    def __init__(self, name, ring_buffer_size=10, failure_rate_threshold=50.0, minimum_number_of_calls=5, ignore_exceptions=None, record_exceptions=None):
        self.name = name
        self.ring_buffer_size = ring_buffer_size
        self.failure_rate_threshold = failure_rate_threshold
        self.minimum_number_of_calls = minimum_number_of_calls
        self.ignore_exceptions = ignore_exceptions or []
        self.record_exceptions = record_exceptions or []
        
        self.state = "CLOSED"
        self.calls = []

    def __repr__(self):
        return f"CircuitBreaker({self.name}) [State: {self.state}]"

    def record_result(self, is_failure):
        if len(self.calls) >= self.ring_buffer_size:
            self.calls.pop(0)
        self.calls.append(1 if is_failure else 0)
        self.evaluate_state()

    def evaluate_state(self):
        if len(self.calls) < self.minimum_number_of_calls:
            return
        failures = sum(self.calls)
        total = len(self.calls)
        failure_rate = (failures / total) * 100
        if failure_rate >= self.failure_rate_threshold:
            self.state = "OPEN"

    def execute(self, func, *args, **kwargs):
        if self.state == "OPEN":
            raise CallNotPermittedException("Circuit breaker is OPEN!")
        
        try:
            result = func(*args, **kwargs)
            self.record_result(is_failure=False)
            return result
        except Exception as e:
            if any(isinstance(e, exc) for exc in self.ignore_exceptions):
                # Bo qua, khong tinh la failure
                raise e
            elif any(isinstance(e, exc) for exc in self.record_exceptions):
                self.record_result(is_failure=True)
                raise e
            else:
                self.record_result(is_failure=False)
                raise e

def mock_wallet_call(error_type):
    if error_type == "insufficient":
        raise InsufficientBalanceException("Khach hang khong du tien")
    elif error_type == "timeout":
        raise TimeoutException("He thống treo mang")
    return "Success"

if __name__ == "__main__":
    cb = CircuitBreaker(
        name="ewalletClient",
        ring_buffer_size=10,
        failure_rate_threshold=50.0,
        minimum_number_of_calls=5,
        ignore_exceptions=[InsufficientBalanceException],
        record_exceptions=[TimeoutException]
    )

    print("--- 1. Gui 8 request InsufficientBalanceException ---")
    for i in range(8):
        try:
            cb.execute(mock_wallet_call, "insufficient")
        except InsufficientBalanceException:
            pass
    print(f"Trang thai hien tai: {cb.state} (Dung la CLOSED vi bi phot lo)")

    print("\n--- 2. Gui lien tiep 5 request TimeoutException ---")
    for i in range(5):
        try:
            cb.execute(mock_wallet_call, "timeout")
        except TimeoutException:
            pass
    print(f"Trang thai hien tai: {cb.state} (Dung la OPEN do loi vuot nguong 50%)")

    print(
        "\n--- 3. Khi mach dang OPEN, gui request hop le hoac loi bat ky ---")
    try:
        cb.execute(mock_wallet_call, "success")
    except CallNotPermittedException as e:
        print(f"Bat duoc ngoai le thanh cong: {e}")