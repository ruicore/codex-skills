#!/usr/bin/env node

import { randomUUID } from "node:crypto";
import { existsSync, mkdirSync, copyFileSync, statSync, readFileSync } from "node:fs";
import { basename, extname, join, relative, resolve } from "node:path";
import { DatabaseSync } from "node:sqlite";

const DEFAULT_APP_DIR = process.env.GENMEDIA_MINI_APP_DIR ?? "";

function usage() {
  console.log(`Usage:
  import-to-mini-app.mjs [options] <file...>

Options:
  --app-dir <path>       Mini app directory. Defaults to GENMEDIA_MINI_APP_DIR.
  --prompt <text>        Prompt to show in the grid.
  --endpoint-id <id>     fal endpoint id.
  --model-name <name>    Human-readable model name.
  --category <name>      Generation category.
  --receipt <path>       Optional genmedia JSON receipt to store with the row.

Example:
  node import-to-mini-app.mjs --prompt "a cat on the moon" --endpoint-id fal-ai/flux/dev ./outputs/image.png
`);
}

function parseArgs(argv) {
  const options = {
    appDir: DEFAULT_APP_DIR,
    prompt: "genmedia output",
    endpointId: "genmedia/local",
    modelName: "genmedia",
    category: "generated-media",
    receipt: null,
    files: [],
  };

  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    const next = argv[index + 1];

    if (arg === "--help" || arg === "-h") {
      usage();
      process.exit(0);
    }

    if (arg === "--app-dir" && next) {
      options.appDir = next;
      index += 1;
    } else if (arg === "--prompt" && next) {
      options.prompt = next;
      index += 1;
    } else if (arg === "--endpoint-id" && next) {
      options.endpointId = next;
      index += 1;
    } else if (arg === "--model-name" && next) {
      options.modelName = next;
      index += 1;
    } else if (arg === "--category" && next) {
      options.category = next;
      index += 1;
    } else if (arg === "--receipt" && next) {
      options.receipt = next;
      index += 1;
    } else if (arg?.startsWith("--")) {
      throw new Error(`Unknown option: ${arg}`);
    } else if (arg) {
      options.files.push(arg);
    }
  }

  return options;
}

function nowIso() {
  return new Date().toISOString();
}

function sanitizeFilename(filename) {
  return filename.replace(/[^a-zA-Z0-9._-]+/g, "-").replace(/^-+|-+$/g, "") || "file";
}

function storagePublicPath(storageKey) {
  return `/api/storage/${storageKey.split("/").map(encodeURIComponent).join("/")}`;
}

function mimeTypeFromFilename(filename) {
  const ext = extname(filename).toLowerCase();
  const map = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".gif": "image/gif",
    ".mp4": "video/mp4",
    ".mov": "video/quicktime",
    ".webm": "video/webm",
    ".mp3": "audio/mpeg",
    ".wav": "audio/wav",
    ".glb": "model/gltf-binary",
    ".json": "application/json",
  };
  return map[ext] ?? "application/octet-stream";
}

function mediaTypeFromFile(filename) {
  const mime = mimeTypeFromFilename(filename);
  if (mime.startsWith("image/")) return "image";
  if (mime.startsWith("video/")) return "video";
  if (mime.startsWith("audio/")) return "audio";
  if (mime.includes("gltf") || filename.endsWith(".glb")) return "3d";
  return "file";
}

function ensureDb(dbPath) {
  const db = new DatabaseSync(dbPath);
  db.exec(`
    PRAGMA journal_mode = WAL;
    CREATE TABLE IF NOT EXISTS generations (
      id TEXT PRIMARY KEY,
      endpoint_id TEXT NOT NULL,
      model_name TEXT,
      category TEXT,
      prompt TEXT NOT NULL,
      status TEXT NOT NULL,
      request_id TEXT,
      params_json TEXT NOT NULL,
      submit_json TEXT,
      result_json TEXT,
      error TEXT,
      created_at TEXT NOT NULL,
      updated_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS assets (
      id TEXT PRIMARY KEY,
      generation_id TEXT,
      kind TEXT NOT NULL,
      media_type TEXT NOT NULL,
      mime_type TEXT,
      filename TEXT NOT NULL,
      storage_key TEXT NOT NULL UNIQUE,
      public_path TEXT NOT NULL,
      source_url TEXT,
      bytes INTEGER NOT NULL,
      created_at TEXT NOT NULL,
      FOREIGN KEY (generation_id) REFERENCES generations(id)
    );
    CREATE INDEX IF NOT EXISTS idx_generations_created_at ON generations(created_at DESC);
    CREATE INDEX IF NOT EXISTS idx_assets_generation_id ON assets(generation_id);
  `);
  return db;
}

function readReceipt(receiptPath) {
  if (!receiptPath) return null;
  const resolved = resolve(receiptPath);
  if (!existsSync(resolved)) {
    throw new Error(`Receipt not found: ${resolved}`);
  }
  return JSON.parse(readFileSync(resolved, "utf8"));
}

function main() {
  const options = parseArgs(process.argv.slice(2));
  if (options.files.length === 0) {
    usage();
    process.exit(1);
  }
  if (!options.appDir) {
    throw new Error("Missing mini app directory. Pass --app-dir or set GENMEDIA_MINI_APP_DIR.");
  }

  const appDir = resolve(options.appDir);
  const dataDir = join(appDir, ".genmedia-studio");
  const bucketDir = join(dataDir, "bucket");
  const generationsDir = join(bucketDir, "generations");
  const dbPath = join(dataDir, "studio.sqlite");

  mkdirSync(generationsDir, { recursive: true });

  const db = ensureDb(dbPath);
  const id = randomUUID();
  const now = nowIso();
  const generationDir = join(generationsDir, id);
  const receipt = readReceipt(options.receipt);

  mkdirSync(generationDir, { recursive: true });

  const params = {
    prompt: options.prompt,
    imported_by: "genmedia-skill",
    imported_files: options.files.map((file) => resolve(file)),
  };

  db.prepare(
    `INSERT INTO generations
     (id, endpoint_id, model_name, category, prompt, status, request_id, params_json, submit_json, result_json, error, created_at, updated_at)
     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
  ).run(
    id,
    options.endpointId,
    options.modelName,
    options.category,
    options.prompt,
    "completed",
    receipt?.request_id ?? receipt?.requestId ?? null,
    JSON.stringify(params),
    receipt ? JSON.stringify(receipt) : null,
    JSON.stringify({ imported_by: "genmedia-skill", receipt_path: options.receipt }),
    null,
    now,
    now,
  );

  const assets = [];
  for (const [index, inputFile] of options.files.entries()) {
    const source = resolve(inputFile);
    if (!existsSync(source)) {
      throw new Error(`File not found: ${source}`);
    }

    const filename = `${id}_${index}-${sanitizeFilename(basename(source))}`;
    const destination = join(generationDir, filename);
    copyFileSync(source, destination);

    const storageKey = relative(bucketDir, destination).split("\\").join("/");
    const stats = statSync(destination);
    const asset = {
      id: randomUUID(),
      generation_id: id,
      kind: "output",
      media_type: mediaTypeFromFile(filename),
      mime_type: mimeTypeFromFilename(filename),
      filename,
      storage_key: storageKey,
      public_path: storagePublicPath(storageKey),
      source_url: null,
      bytes: stats.size,
      created_at: now,
    };

    db.prepare(
      `INSERT INTO assets
       (id, generation_id, kind, media_type, mime_type, filename, storage_key, public_path, source_url, bytes, created_at)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
    ).run(
      asset.id,
      asset.generation_id,
      asset.kind,
      asset.media_type,
      asset.mime_type,
      asset.filename,
      asset.storage_key,
      asset.public_path,
      asset.source_url,
      asset.bytes,
      asset.created_at,
    );

    assets.push(asset);
  }

  console.log(
    JSON.stringify(
      {
        app_url: "http://localhost:3000/",
        generation: {
          id,
          endpoint_id: options.endpointId,
          model_name: options.modelName,
          category: options.category,
          prompt: options.prompt,
          status: "completed",
          assets,
        },
      },
      null,
      2,
    ),
  );
}

try {
  main();
} catch (error) {
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
}
