const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");
const interSrc = path.join(root, "node_modules", "@fontsource", "inter", "files");
const symbolsSrc = path.join(root, "node_modules", "material-symbols");
const interDest = path.join(root, "app", "static", "fonts", "inter");
const symbolsDest = path.join(root, "app", "static", "fonts", "material-symbols");

fs.mkdirSync(interDest, { recursive: true });
fs.mkdirSync(symbolsDest, { recursive: true });

const interWeights = ["400", "600", "700"];
for (const weight of interWeights) {
  const filename = `inter-latin-${weight}-normal.woff2`;
  fs.copyFileSync(path.join(interSrc, filename), path.join(interDest, filename));
}

fs.copyFileSync(
  path.join(symbolsSrc, "material-symbols-outlined.woff2"),
  path.join(symbolsDest, "material-symbols-outlined.woff2")
);

console.log("Fonts copied to app/static/fonts");
