/*
  @license
	Rollup.js v4.53.1
	Fri, 07 Nov 2025 21:55:39 GMT - commit e3bdcdfe5633a6835dc4c61f8cf93a682406d965

	https://github.com/rollup/rollup

	Released under the MIT License.
*/
export { version as VERSION, defineConfig, rollup, watch } from './shared/node-entry.js';
import './shared/parseAst.js';
import '../native.js';
import 'node:path';
import 'path';
import 'node:process';
import 'node:perf_hooks';
import 'node:fs/promises';
