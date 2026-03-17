#!/usr/bin/env node
"use strict";

const readline = require("readline");
const { calculate } = require("./calculator");

// ── Helpers ────────────────────────────────────────────────────────────────

const OPERATIONS = ["add", "subtract", "multiply", "divide"];
const ALIASES = { "+": "add", "-": "subtract", "*": "multiply", "/": "divide" };

function parseArgs(argv) {
  // Support:  calc <op> <a> <b>  (non-interactive mode)
  const [, , op, a, b] = argv;
  return { op, a, b };
}

function formatResult(op, a, b, result) {
  const symbols = { add: "+", subtract: "−", multiply: "×", divide: "÷" };
  return `  ${a} ${symbols[op]} ${b} = ${result}`;
}

function runOnce(opRaw, aRaw, bRaw) {
  const op = ALIASES[opRaw] || opRaw;
  const a = parseFloat(aRaw);
  const b = parseFloat(bRaw);

  if (!OPERATIONS.includes(op)) {
    console.error(`✖  Unknown operation "${opRaw}". Use: add, subtract, multiply, divide (or +, -, *, /)`);
    process.exit(1);
  }
  if (isNaN(a) || isNaN(b)) {
    console.error(`✖  Both operands must be valid numbers. Got: "${aRaw}", "${bRaw}"`);
    process.exit(1);
  }

  try {
    const result = calculate(op, a, b);
    console.log(formatResult(op, a, b, result));
  } catch (err) {
    console.error(`✖  ${err.message}`);
    process.exit(1);
  }
}

// ── Interactive REPL ───────────────────────────────────────────────────────

function startRepl() {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
    prompt: "calc> ",
  });

  console.log("╔══════════════════════════════════════╗");
  console.log("║       CLI Calculator  🧮              ║");
  console.log("╠══════════════════════════════════════╣");
  console.log("║  Usage:  <op> <a> <b>                ║");
  console.log("║  Ops:    add  subtract  multiply      ║");
  console.log("║          divide  (or  +  -  *  /)    ║");
  console.log("║  Type  help  or  exit  to quit        ║");
  console.log("╚══════════════════════════════════════╝");
  console.log();

  rl.prompt();

  rl.on("line", (line) => {
    const trimmed = line.trim();
    if (!trimmed) { rl.prompt(); return; }

    if (trimmed === "exit" || trimmed === "quit") {
      console.log("Goodbye! 👋");
      rl.close();
      return;
    }

    if (trimmed === "help") {
      console.log("  Operations : add (+)  subtract (-)  multiply (*)  divide (/)");
      console.log("  Example    : add 10 5   →   10 + 5 = 15");
      console.log("  Example    : / 9 3      →   9 ÷ 3 = 3");
      rl.prompt();
      return;
    }

    const parts = trimmed.split(/\s+/);
    if (parts.length !== 3) {
      console.error("  ✖  Expected exactly 3 tokens: <op> <a> <b>");
      rl.prompt();
      return;
    }

    const [opRaw, aRaw, bRaw] = parts;
    const op = ALIASES[opRaw] || opRaw;
    const a = parseFloat(aRaw);
    const b = parseFloat(bRaw);

    if (!OPERATIONS.includes(op)) {
      console.error(`  ✖  Unknown operation "${opRaw}".`);
      rl.prompt();
      return;
    }
    if (isNaN(a) || isNaN(b)) {
      console.error(`  ✖  Both operands must be valid numbers. Got: "${aRaw}", "${bRaw}"`);
      rl.prompt();
      return;
    }

    try {
      const result = calculate(op, a, b);
      console.log(formatResult(op, a, b, result));
    } catch (err) {
      console.error(`  ✖  ${err.message}`);
    }

    rl.prompt();
  });

  rl.on("close", () => process.exit(0));
}

// ── Entry point ────────────────────────────────────────────────────────────

const { op, a, b } = parseArgs(process.argv);

if (op && a && b) {
  // Non-interactive: calc add 10 5
  runOnce(op, a, b);
} else if (op || a || b) {
  console.error("✖  Non-interactive mode requires exactly 3 arguments: <op> <a> <b>");
  console.error("   Example: node index.js add 10 5");
  process.exit(1);
} else {
  // Launch interactive REPL
  startRepl();
}
