#!/usr/bin/env node
// Upload a local image to kie.ai's file endpoint and print the hosted URL.
// kie_image's `image_input` requires PUBLIC http(s) URLs — local paths,
// file:// and data: URIs are all rejected. This keeps the photo within the
// kie.ai vendor (no third-party host).
//
// Usage: node upload-reference.mjs "<local-image-path>" [maxWidth=768]
// Requires: KIE_API_KEY in robOS .env, Python+PIL for resize (optional).
//
// Prints the downloadUrl on success (last line of stdout).

import fs from 'fs';
import { execSync } from 'child_process';
import path from 'path';

const src = process.argv[2];
const maxW = parseInt(process.argv[3] || '768', 10);
if (!src || !fs.existsSync(src)) {
  console.error('Usage: node upload-reference.mjs "<local-image-path>" [maxWidth]');
  process.exit(1);
}

// Resolve KIE_API_KEY from robOS .env
const envPath = path.resolve(process.cwd(), '.env');
const env = fs.readFileSync(envPath, 'utf8');
const key = (env.match(/^KIE_API_KEY=(.+)$/m) || [])[1]?.trim();
if (!key) { console.error('KIE_API_KEY missing in .env'); process.exit(1); }

// Resize via PIL to keep payload small (face reference needs no full res).
// Falls back to raw bytes if Python/PIL unavailable.
let b64;
try {
  const py = [
    'from PIL import Image; import base64,io,sys',
    `im=Image.open(r'''${src}''').convert('RGB')`,
    `w=${maxW}; h=int(im.height*w/im.width)`,
    'im=im.resize((w,h), Image.LANCZOS)',
    'buf=io.BytesIO(); im.save(buf,format="JPEG",quality=85)',
    'sys.stdout.write(base64.b64encode(buf.getvalue()).decode())',
  ].join('\n');
  b64 = execSync(`python -c ${JSON.stringify(py)}`, { maxBuffer: 64 * 1024 * 1024 }).toString().trim();
} catch {
  b64 = fs.readFileSync(src).toString('base64');
}

const body = JSON.stringify({
  base64Data: 'data:image/jpeg;base64,' + b64,
  uploadPath: 'images/user-upload',
  fileName: path.basename(src).replace(/[^\w.\-]/g, '_'),
});

const r = await fetch('https://kieai.redpandaai.co/api/file-base64-upload', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', Authorization: 'Bearer ' + key },
  body,
});
const j = await r.json().catch(() => null);
if (!r.ok || !j?.data?.downloadUrl) {
  console.error('Upload failed:', r.status, JSON.stringify(j));
  process.exit(1);
}
console.log(j.data.downloadUrl);
