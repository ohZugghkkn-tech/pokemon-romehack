const assert = require('node:assert/strict');
const test = require('node:test');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { expandIncludes, stageSources } = require('./compile.cjs');

test('shared declarations are kept in both isolated stages', () => {
  const result = stageSources('#version 450\n#pragma stage vertex\nvoid vertex() {}\n#pragma stage fragment\nvoid fragment() {}\n');
  assert.ok(result.vertex.startsWith('#version 450'));
  assert.ok(result.fragment.startsWith('#version 450'));
  assert.ok(!result.vertex.includes('void fragment'));
  assert.ok(!result.fragment.includes('void vertex'));
});

test('missing, reordered and duplicate stages fail', () => {
  for (const input of ['', '#pragma stage fragment\n#pragma stage vertex\n',
    '#pragma stage vertex\n#pragma stage vertex\n#pragma stage fragment\n']) {
    assert.throws(() => stageSources(input), /Expected/);
  }
});

test('includes resolve locally and reject cycles and traversal', () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'shader-includes-'));
  try {
    const file = path.join(root, 'main.slang');
    fs.writeFileSync(file, '#include "shared.h"\n');
    fs.writeFileSync(path.join(root, 'shared.h'), 'float value;\n');
    assert.match(expandIncludes(file, root), /float value;/);
    fs.writeFileSync(path.join(root, 'shared.h'), '#include "main.slang"\n');
    assert.throws(() => expandIncludes(file, root), /Cyclic/);
    fs.writeFileSync(file, '#include "../outside.h"\n');
    assert.throws(() => expandIncludes(file, root), /escapes/);
  } finally {
    fs.rmSync(root, { recursive: true });
  }
});
