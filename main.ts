// gta6-meme-x-01 entry (Node 22, standard library only): it copies POST.json
// from the repository root to /output/POST.json, where the gate reads it.
// The entry is the post itself — a GTA 6 meme posted on X from a public
// account. The meme: a Vice City street at dusk, the make.fun ghost walking
// with two characters, captioned "WAITED 13 YEARS FOR GTA 6 / MY AGENT GOT
// PAID ON MAKE.FUN". The post's text carries the make.fun bounty link and
// the play code, and POST.json names the post's address.
//
// Before copying, this program reads POST.json and checks the address is a
// real X post URL (https://x.com/<handle>/status/<id>). A placeholder or a
// non-X address is refused here, so a bad POST.json fails loudly instead of
// being copied through and refused later by the gate.
//
// Outside the grader's container, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR
// stand in for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

const postPath = join(BOT_DIR, 'POST.json');
let postUrl: string;
try {
  postUrl = JSON.parse(readFileSync(postPath, 'utf8')).url;
} catch (err) {
  console.error(`POST.json could not be read from ${BOT_DIR}: ${(err as Error).message}`);
  process.exit(1);
}
if (typeof postUrl !== 'string' || !/^https:\/\/(x\.com|twitter\.com)\/\w+\/status\/\d+/.test(postUrl)) {
  console.error(`POST.json does not name a public X post URL: ${String(postUrl)}`);
  process.exit(1);
}
console.log(`Entry post: ${postUrl}`);

mkdirSync(OUTPUT_DIR, { recursive: true });
try {
  copyFileSync(postPath, join(OUTPUT_DIR, 'POST.json'));
} catch (err) {
  console.error(`POST.json could not be copied from ${BOT_DIR}: ${(err as Error).message}`);
  process.exit(1);
}
