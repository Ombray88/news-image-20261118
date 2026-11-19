import * as fs from 'fs';
import * as path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const outputDir = process.env.MAKEFUN_OUTPUT_DIR || '/output';
if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
}

const sourcePath = path.join(__dirname, 'entry.png');
const destPath = path.join(outputDir, 'entry.png');

const data = fs.readFileSync(sourcePath);
fs.writeFileSync(destPath, data);

const stats = fs.statSync(destPath);
console.log(`Output path: ${destPath}`);
console.log(`File size: ${stats.size} bytes`);
