import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { execFileSync } from 'node:child_process';

const [inputMd, outputMd, outputDir] = process.argv.slice(2);

if (!inputMd || !outputMd || !outputDir) {
  console.error('Usage: node scripts/render_mermaid_md.mjs <input.md> <output.md> <output-dir>');
  process.exit(1);
}

const inputPath = path.resolve(inputMd);
const outputPath = path.resolve(outputMd);
const assetsDir = path.resolve(outputDir);

fs.mkdirSync(assetsDir, { recursive: true });

const markdown = fs.readFileSync(inputPath, 'utf8');
const blockPattern = /```mermaid\s*\n([\s\S]*?)```/g;

let diagramIndex = 0;
let lastIndex = 0;
let renderedMarkdown = '';

for (const match of markdown.matchAll(blockPattern)) {
  const [fullMatch, mermaidCode] = match;
  const matchIndex = match.index ?? 0;
  diagramIndex += 1;

  renderedMarkdown += markdown.slice(lastIndex, matchIndex);

  const nameBase = `diagram-${String(diagramIndex).padStart(2, '0')}`;
  const tempMmd = path.join(os.tmpdir(), `${nameBase}.mmd`);
  const tempPng = path.join(assetsDir, `${nameBase}.png`);

  fs.writeFileSync(tempMmd, mermaidCode.trimStart(), 'utf8');

  const command = process.platform === 'win32' ? 'cmd' : 'npx';
  const args = process.platform === 'win32'
    ? ['/c', 'npx', '-y', '@mermaid-js/mermaid-cli', '-i', tempMmd, '-o', tempPng, '-b', 'white', '-w', '2200']
    : ['-y', '@mermaid-js/mermaid-cli', '-i', tempMmd, '-o', tempPng, '-b', 'white', '-w', '2200'];
  execFileSync(command, args, { stdio: 'inherit' });

  const relativeImagePath = path.relative(path.dirname(outputPath), tempPng).split(path.sep).join('/');
  const imageWidth = diagramIndex === 2 ? '85%' : '70%';
  renderedMarkdown += `\n\n![Mermaid diagram ${diagramIndex}](${relativeImagePath}){ width=${imageWidth} }\n\n`;
  lastIndex = matchIndex + fullMatch.length;
}

renderedMarkdown += markdown.slice(lastIndex);
fs.writeFileSync(outputPath, renderedMarkdown, 'utf8');
