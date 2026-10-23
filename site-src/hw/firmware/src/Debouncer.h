#pragma once
#include <stdint.h>

// Pure logic: ไม่เรียก Arduino API เลย จึง test บน PC ได้
class Debouncer {
public:
  enum class Event : uint8_t { None, Pressed, Released };

  explicit Debouncer(uint32_t stableMs = 20) : stableMs_(stableMs) {}

  // raw: true = กดอยู่ (แปลง active-LOW มาแล้ว), nowMs: เวลาปัจจุบัน
  Event update(bool raw, uint32_t nowMs) {
    if (raw != lastRaw_) {  // ยังเด้งอยู่ → เริ่มจับเวลาใหม่
      lastRaw_ = raw;
      changedAt_ = nowMs;
      return Event::None;
    }
    if (raw != stable_ && (nowMs - changedAt_) >= stableMs_) {
      stable_ = raw;
      return stable_ ? Event::Pressed : Event::Released;
    }
    return Event::None;
  }

  bool isPressed() const { return stable_; }

private:
  uint32_t stableMs_;
  uint32_t changedAt_ = 0;
  bool lastRaw_ = false;
  bool stable_ = false;
};
