// Compile the preset's shaders, not just the file references. No GPU required.
const fs = require('node:fs');
const path = require('node:path');
const ROOT = path.resolve(__dirname, '../../shaders');

function expandIncludes(file, root = ROOT, stack = []) {
  file = path.resolve(file);
  const relative = path.relative(root, file);
  if (relative === '..' || relative.startsWith(`..${path.sep}`) || path.isAbsolute(relative)) {
    throw new Error(`Include escapes shader directory: ${file}`);
  }
  if (stack.includes(file)) throw new Error(`Cyclic shader include: ${file}`);
  return fs.readFileSync(file, 'utf8').replace(
    /^\s*#include\s+"([^"]+)"/gm,
    (_, include) => expandIncludes(path.resolve(path.dirname(file), include), root, [...stack, file]),
  );
}

function stageSources(source) {
  const vertex = [...source.matchAll(/^\s*#pragma stage vertex\s*$/gm)];
  const fragment = [...source.matchAll(/^\s*#pragma stage fragment\s*$/gm)];
  if (vertex.length !== 1 || fragment.length !== 1 || vertex[0].index >= fragment[0].index) {
    throw new Error('Expected one vertex section followed by one fragment section');
  }
  const v = vertex[0].index, f = fragment[0].index;
  const common = source.slice(0, v);
  return { vertex: common + source.slice(v, f), fragment: common + source.slice(f) };
}

function main() {
  const glslang = require('@webgpu/glslang')();
  const preset = fs.readFileSync(path.join(ROOT, 'soulgold-vivid-relief.slangp'), 'utf8');
  const declared = Number(preset.match(/^shaders\s*=\s*(\d+)$/m)?.[1]);
  const entries = [...preset.matchAll(/^shader(\d+)\s*=\s*([^\r\n]+)$/gm)];
  if (!declared || entries.length !== declared) throw new Error('Incomplete shader chain');
  let count = 0;
  for (let i = 0; i < declared; i++) {
    const entry = entries.find(match => Number(match[1]) === i);
    if (!entry) throw new Error(`Missing shader${i}`);
    const file = entry[2].trim().replace(/^"|"$/g, '');
    const stages = stageSources(expandIncludes(path.join(ROOT, file)));
    for (const [stage, source] of Object.entries(stages)) {
      const words = glslang.compileGLSL(source, stage);
      if (!words.length || words[0] !== 0x07230203) throw new Error(`Invalid SPIR-V: ${file}`);
      console.log(`Compiled ${file} (${stage}, ${words.length} SPIR-V words)`);
      count++;
    }
  }
  console.log(`${count} stages compiled; no GPU execution, reflection/link validation or visual approval implied.`);
}

module.exports = { expandIncludes, stageSources };
if (require.main === module) main();
