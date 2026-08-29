// Booking error hierarchy — extend BookingError for new failure kinds.
export class BookingError extends Error {}
export class BookingConflictError extends BookingError {}
export class InvalidIntervalError extends BookingError {}
