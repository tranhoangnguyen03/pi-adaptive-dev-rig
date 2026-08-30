// Example caller — how the rest of the repo uses BookingBook.
import { BookingBook } from "./booking.js";
import { BookingConflictError } from "./errors.js";

export function morning(book) {
  book.add("standup", { start: 9, end: 9.5 });
  try {
    book.add("review", { start: 9, end: 10 });
  } catch (e) {
    if (!(e instanceof BookingConflictError)) throw e;
    book.add("review", { start: 10, end: 11 });
  }
  return book.list();
}

export { BookingBook };
