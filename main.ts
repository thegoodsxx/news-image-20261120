const fs = require("node:fs");
const path = require("node:path");
const process = require("node:process");

/**
 * Entry runner for news-image-20261120 make.fun competition.
 * Copies the pre-rendered entry poster to the designated output directory.
 */
function deliverEntry(): void {
  const outputDir: string = process.env.MAKEFUN_OUTPUT_DIR || "/output";
  const sourceImage: string = path.resolve(process.cwd(), "entry.png");
  const destinationImage: string = path.join(outputDir, "entry.png");

  if (!fs.existsSync(sourceImage)) {
    console.error(`Error: source image not found at ${sourceImage}`);
    process.exit(1);
  }

  try {
    fs.mkdirSync(outputDir, { recursive: true });
    fs.copyFileSync(sourceImage, destinationImage);

    const stats = fs.statSync(destinationImage);
    console.log(`Successfully delivered entry to ${destinationImage} (${stats.size} bytes).`);
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : String(err);
    console.error(`Failed to copy entry image: ${message}`);
    process.exit(1);
  }
}

deliverEntry();
