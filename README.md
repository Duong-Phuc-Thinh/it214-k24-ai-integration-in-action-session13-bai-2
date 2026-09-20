# Thuc hanh Circuit Breaker voi Resilience4j (Mo phong Python)

Du an nay mo phong cau hinh cua so truot Count-Based va bay ngoai le nghiep vu (giua Checkout-Service va EWallet-Service).

## Chuc nang da lam
- Mo phong lop CircuitBreaker voi Count-Based Sliding Window.
- Cau hinh nguong loi (failure rate threshold = 50%), so request toi thieu (minimumNumberOfCalls = 5).
- Bo qua loi InsufficientBalanceException (khong tinh vao circuit breaker).
- Ghi nhan loi TimeoutException de kich hoat trang thai OPEN.

## Huong dan chay chuong trinh
Chay file main.py bang lenh:
python main.py