#!/usr/bin/env node

const { join } = require('path');
const { readdirSync, readFileSync, statSync, writeFileSync } = require('fs');

const { version } = require(join(__dirname, 'version.json'));
const calVer = /\/\d{4}\.\d{1,2}\.\d{1,2}\//g;

const patch = directory => {
  for (const file of readdirSync(directory)) {
    const path = join(directory, file);
    if (file.endsWith('.md') || file.endsWith('.html')) {
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

// Download and extract PyScript source code for the current version.
const { execSync } = require('child_process');
const { mkdtempSync, rmSync, cpSync } = require('fs');
const { tmpdir } = require('os');

const downloadFileSync = (url, destination) => {
  // Use curl which is available on Mac and Linux.
  try {
    execSync(`curl -L -o "${destination}" "${url}"`, { 
      stdio: 'ignore' 
    });
  } catch (error) {
    throw new Error(`Download failed: ${error.message}`);
  }
};

const updatePyScriptSource = () => {
  const url = `https://github.com/pyscript/pyscript/archive/refs/tags/${version}.zip`;
  const tempDir = mkdtempSync(join(tmpdir(), 'pyscript-'));
  const zipPath = join(tempDir, `pyscript-${version}.zip`);
  const targetDir = join(__dirname, 'pyscript');

  try {
    console.log(`Downloading PyScript ${version}...`);
    downloadFileSync(url, zipPath);

    console.log('Extracting archive...');
    execSync(`unzip -q "${zipPath}" -d "${tempDir}"`);

    const sourceDir = join(
      tempDir,
      `pyscript-${version}`,
      'core',
      'src',
      'stdlib',
      'pyscript'
    );

    if (!statSync(sourceDir, { throwIfNoEntry: false })?.isDirectory()) {
      throw new Error(`Expected directory not found: ${sourceDir}`);
    }

    console.log('Copying PyScript stdlib files...');
    cpSync(sourceDir, targetDir, { recursive: true, force: true });

    console.log('PyScript source updated successfully.');
  } catch (error) {
    console.error('Error updating PyScript source:', error.message);
    process.exit(1);
  } finally {
    console.log('Cleaning up temporary files...');
    rmSync(tempDir, { recursive: true, force: true });
  }
};

updatePyScriptSource();
