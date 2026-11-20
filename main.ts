import { copyFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

/**
 * Entry runner for news-image-20261120 make.fun competition.
 * Delivers entry.png to the designated output directory.
 */
function deliverEntry(): void {
  const scriptDir: string = dirname(fileURLToPath(import.meta.url));
  const sourceImage: string = join(scriptDir, "entry.png");
  const targetDir: string = process.env.MAKEFUN_OUTPUT_DIR || "/output";
  const targetImage: string = join(targetDir, "entry.png");

  if (!existsSync(sourceImage)) {
    console.error(`Error: source entry image not found at ${sourceImage}`);
    process.exit(1);
  }

  try {
    mkdirSync(targetDir, { recursive: true });
    copyFileSync(sourceImage, targetImage);

    const stats = statSync(targetImage);
    console.log(`Delivered entry.png to ${targetImage} (${stats.size} bytes).`);
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : String(err);
    console.error(`Failed to deliver entry image: ${message}`);
    process.exit(1);
  }
}

deliverEntry();
