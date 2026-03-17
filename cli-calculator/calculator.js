/**
 * Core calculator operations.
 * Each function validates its inputs and returns a numeric result.
 */

function add(a, b) {
  return a + b;
}

function subtract(a, b) {
  return a - b;
}

function multiply(a, b) {
  return a * b;
}

function divide(a, b) {
  if (b === 0) throw new Error("Division by zero is not allowed.");
  return a / b;
}

/**
 * Dispatch an operation by name.
 * @param {string} op  - "add" | "subtract" | "multiply" | "divide"
 * @param {number} a
 * @param {number} b
 * @returns {number}
 */
function calculate(op, a, b) {
  const ops = { add, subtract, multiply, divide };
  if (!ops[op]) throw new Error(`Unknown operation "${op}". Valid: add, subtract, multiply, divide.`);
  return ops[op](a, b);
}

module.exports = { add, subtract, multiply, divide, calculate };
