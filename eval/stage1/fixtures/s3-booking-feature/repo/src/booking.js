// BookingBook — time-slot registry. Deterministic: no clocks; ticks are logical.
import { BookingConflictError, InvalidIntervalError } from "./errors.js";

export class BookingBook {
  #bookings = new Map(); // id -> {start, end}

  add(id, { start, end }) {
    if (!(Number.isFinite(start) && Number.isFinite(end)) || end <= start) {
      throw new InvalidIntervalError(`interval for ${id} must have end > start`);
    }
    for (const b of this.#bookings.values()) {
      if (start < b.end && b.start < end) {
        throw new BookingConflictError(`${id} overlaps ${b}`);
      }
    }
    this.#bookings.set(id, { start, end });
    return { id, start, end };
  }

  cancel(id) {
    return this.#bookings.delete(id);
  }

  list() {
    return [...this.#bookings.values()].sort((a, b) => a.start - b.start);
  }
}
