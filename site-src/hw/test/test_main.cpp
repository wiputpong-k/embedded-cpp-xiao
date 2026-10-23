#include <cstdio>
#include <cstdlib>
#include "RingBuffer.h"
#include "Debouncer.h"

static int failures = 0;
#define CHECK(cond)                                                    \
  do {                                                                 \
    if (!(cond)) {                                                     \
      std::printf("FAIL %s:%d  %s\n", __FILE__, __LINE__, #cond);      \
      ++failures;                                                      \
    }                                                                  \
  } while (0)

static void test_ringbuffer() {
  RingBuffer<int, 3> rb;
  CHECK(rb.size() == 0);
  CHECK(rb.push(1) && rb.push(2) && rb.push(3));
  CHECK(!rb.push(4));          // เต็มแล้ว
  int v = 0;
  CHECK(rb.pop(v) && v == 1);  // FIFO: ออกตัวแรกก่อน
  rb.pushOverwrite(4);
  rb.pushOverwrite(5);         // เต็ม → ทิ้ง 2
  CHECK(rb.at(0) == 3 && rb.at(2) == 5);
  CHECK(average(rb) == 4.0f);
}

static void test_debouncer() {
  using E = Debouncer::Event;
  Debouncer d(20);
  CHECK(d.update(true, 0) == E::None);   // เริ่มกด
  CHECK(d.update(false, 5) == E::None);  // เด้ง
  CHECK(d.update(true, 8) == E::None);   // เด้ง
  CHECK(d.update(true, 20) == E::None);  // นิ่งมาแค่ 12 ms
  CHECK(d.update(true, 28) == E::Pressed);
  CHECK(d.isPressed());
  CHECK(d.update(true, 40) == E::None);  // กดค้าง ไม่ยิงซ้ำ
}

int main() {
  test_ringbuffer();
  test_debouncer();
  if (failures == 0) std::puts("ALL TESTS PASSED");
  return failures == 0 ? EXIT_SUCCESS : EXIT_FAILURE;
}
