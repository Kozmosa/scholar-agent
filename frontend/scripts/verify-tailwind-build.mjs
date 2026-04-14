import { readdir, readFile } from 'node:fs/promises';
import path from 'node:path';
import process from 'node:process';

const distAssetsDir = path.resolve('dist/assets');
const requiredFragments = [
  'padding-inline:calc(var(--spacing)*4)',
  'border-radius:var(--radius-xl)',
  'color:var(--color-gray-900)',
];

function normalizeCss(value) {
  return value.replace(/\s+/g, '');
}

async function main() {
  const assetNames = await readdir(distAssetsDir);
  const cssAssetName = assetNames.find((name) => name.endsWith('.css'));

  if (!cssAssetName) {
    throw new Error(`No CSS asset found in ${distAssetsDir}`);
  }

  const css = await readFile(path.join(distAssetsDir, cssAssetName), 'utf8');
  const normalizedCss = normalizeCss(css);
  const missingFragments = requiredFragments.filter(
    (fragment) => !normalizedCss.includes(normalizeCss(fragment)),
  );

  if (missingFragments.length > 0) {
    throw new Error(
      `Missing Tailwind CSS fragments: ${missingFragments.join(', ')} in ${cssAssetName}`,
    );
  }

  console.log(`Verified Tailwind CSS output in ${cssAssetName}`);
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exitCode = 1;
});
