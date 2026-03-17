/**
 * Lightweight test runner — no external dependencies.
 */
"use strict";

const { add, subtract, multiply, divide, calculate } = require("./calculator");

let passed = 0;
let failed = 0;

function assert(description, actual, expected) {
  if (actual === expected) {
    console.log(`  ✔  ${description}`);
    passed++;
  } else {
    console.error(`  ✖  ${description}`);
    console.error(`       expected: ${expected}`);
    console.error(`       actual  : ${actual}`);
    failed++;
  }
}

function assertThrows(description, fn, expectedMsg) {
  try {
    fn();
    console.error(`  ✖  ${description}  (no error thrown)`);
    failed++;
  } catch (err) {
    if (err.message.includes(expectedMsg)) {
      console.log(`  ✔  ${description}`);
      passed++;
    } else {
      console.error(`  ✖  ${description}  (wrong error: "${err.message}")`);
      failed++;
    }
  }
}

// ── Tests ──────────────────────────────────────────────────────────────────

console.log("\nAddition");
assert("2 + 3 = 5",          add(2, 3),       5);
assert("0 + 0 = 0",          add(0, 0),       0);
assert("-1 + 1 = 0",         add(-1, 1),      0);
assert("1.5 + 2.5 = 4",      add(1.5, 2.5),   4);

console.log("\nSubtraction");
assert("10 - 4 = 6",         subtract(10, 4),  6);
assert("0 - 5 = -5",         subtract(0, 5),  -5);
assert("-3 - (-3) = 0",      subtract(-3, -3), 0);

console.log("\nMultiplication");
assert("3 × 4 = 12",         multiply(3, 4),   12);
assert("0 × 999 = 0",        multiply(0, 999),  0);
assert("-2 × 6 = -12",       multiply(-2, 6), -12);

console.log("\nDivision");
assert("10 ÷ 2 = 5",         divide(10, 2),    5);
assert("7 ÷ 2 = 3.5",        divide(7, 2),     3.5);
assert("-9 ÷ 3 = -3",        divide(-9, 3),   -3);
assertThrows("÷ 0 throws",   () => divide(5, 0), "Division by zero");

console.log("\ncalculate() dispatcher");
assert('calculate("add", 1, 2) = 3',      calculate("add",      1, 2),  3);
assert('calculate("subtract", 9, 4) = 5', calculate("subtract", 9, 4),  5);
assert('calculate("multiply", 3, 7) = 21',calculate("multiply", 3, 7), 21);
assert('calculate("divide", 8, 4) = 2',   calculate("divide",   8, 4),  2);
assertThrows("unknown op throws", () => calculate("mod", 5, 2), "Unknown operation");

// ── Summary ────────────────────────────────────────────────────────────────

console.log(`\n${"─".repeat(40)}`);
console.log(`  ${passed} passed  |  ${failed} failed`);
console.log(`${"─".repeat(40)}\n`);

if (failed > 0) process.exit(1);
