#!/usr/bin/env node

const { join } = require('path');
const { readdirSync, readFileSync, statSync, writeFileSync } = require('fs');

const { version } = require(join(__dirname, 'version.json'));
const calVer = /\/\d{4}\.\d{1,2}\.\d{1,2}\//g;

const patch = directory => {
  for (const file of readdirSync(directory)) {
    const path = join(directory, file);
    if (file.endsWith('.md')) {
      writeFileSync(
        path,
        readFileSync(path).toString().replace(
          calVer,
          `/${version}/`
        )
      );
    }
    else if (statSync(path).isDirectory())
      patch(path);
  }
};

patch(join(__dirname, 'docs'));
