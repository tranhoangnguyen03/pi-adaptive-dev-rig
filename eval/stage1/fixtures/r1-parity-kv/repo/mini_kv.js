// Two tiny key-value stores. Same API, same claimed semantics:
//   set(k,v); get(k) -> v | undefined; delete(k) -> had?; keys() -> sorted
// Claimed merge rule: last write wins, EXCEPT deletes win over earlier
// sets (tombstone priority).
class FlatKV {
  #map = new Map();
  set(k, v) { this.#map.set(k, v); }
  delete(k) { return this.#map.delete(k); }
  get(k) { return this.#map.get(k); }
  keys() { return [...this.#map.keys()].sort(); }
}

class LogKV {
  #log = [];  // [op, k, v]
  set(k, v) { this.#log.push(["set", k, v]); }
  delete(k) { this.#log.push(["del", k]); }
  get(k) {
    let v;
    for (const [op, key, val] of this.#log) {
      if (key !== k) continue;
      if (op === "set") v = val; else v = undefined;  // del = tombstone
    }
    return v;
  }
  keys() {
    const out = new Set();
    for (const [op, key] of this.#log) { if (op === "set") out.add(key); else out.delete(key); }
    return [...out].sort();
  }
}

export { FlatKV, LogKV };
