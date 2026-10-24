#pragma once
#include <stddef.h>

// core ของ Seeed nRF52 มี class RingBuffer อยู่แล้ว จึงต้องอยู่ใน namespace ไม่ให้ชื่อชนกัน
namespace xiao {

// FIFO ขนาดคงที่ ไม่ใช้ heap — ขนาด N ถูกกำหนดตอน compile
template <typename T, size_t N>
class RingBuffer {
  static_assert(N > 0, "N must be > 0");

public:
  bool push(const T& v) {
    if (count_ == N) return false;  // เต็ม
    buf_[head_] = v;
    head_ = (head_ + 1) % N;
    ++count_;
    return true;
  }

  bool pop(T& out) {
    if (count_ == 0) return false;  // ว่าง
    out = buf_[tail_];
    tail_ = (tail_ + 1) % N;
    --count_;
    return true;
  }

  // เต็มแล้วให้ทิ้งตัวเก่าสุด (เหมาะกับ moving average)
  void pushOverwrite(const T& v) {
    if (count_ == N) {
      T dropped;
      pop(dropped);
    }
    push(v);
  }

  size_t size() const { return count_; }
  bool full() const { return count_ == N; }
  const T& at(size_t i) const { return buf_[(tail_ + i) % N]; }  // 0 = เก่าสุด

private:
  T buf_[N]{};
  size_t head_ = 0, tail_ = 0, count_ = 0;
};

template <typename T, size_t N>
float average(const RingBuffer<T, N>& rb) {
  if (rb.size() == 0) return 0.0f;
  float sum = 0;
  for (size_t i = 0; i < rb.size(); ++i) sum += rb.at(i);
  return sum / rb.size();
}

}  // namespace xiao
