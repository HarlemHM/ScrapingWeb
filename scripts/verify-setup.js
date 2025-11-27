#!/usr/bin/env node

/**
 * Script de verificación de setup para Pymes Hoteleras
 * Verifica que todas las dependencias estén instaladas correctamente
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

console.log('🔍 Verificando setup del proyecto Pymes Hoteleras...\n');

// Colores para output
const colors = {
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  reset: '\x1b[0m'
};

function logSuccess(message) {
  console.log(`${colors.green}✅ ${message}${colors.reset}`);
}

function logError(message) {
  console.log(`${colors.red}❌ ${message}${colors.reset}`);
}

function logWarning(message) {
  console.log(`${colors.yellow}⚠️  ${message}${colors.reset}`);
}

function logInfo(message) {
  console.log(`${colors.blue}ℹ️  ${message}${colors.reset}`);
}

// Verificar Node.js
try {
  const nodeVersion = execSync('node --version', { encoding: 'utf8' }).trim();
  const majorVersion = parseInt(nodeVersion.slice(1).split('.')[0]);
  
  if (majorVersion >= 16) {
    logSuccess(`Node.js ${nodeVersion} instalado correctamente`);
  } else {
    logError(`Node.js ${nodeVersion} instalado, pero se requiere versión 16+`);
    process.exit(1);
  }
} catch (error) {
  logError('Node.js no está instalado o no está en el PATH');
  process.exit(1);
}

// Verificar npm
try {
  const npmVersion = execSync('npm --version', { encoding: 'utf8' }).trim();
  logSuccess(`npm ${npmVersion} instalado correctamente`);
} catch (error) {
  logError('npm no está instalado o no está en el PATH');
  process.exit(1);
}

// Verificar archivos del proyecto
const requiredFiles = [
  'package.json',
  'src/App.tsx',
  'src/data/hotels.json',
  'src/data/reviews.json',
  'src/data/config.json',
  'vite.config.ts'
];

console.log('\n📁 Verificando archivos del proyecto...');
let allFilesExist = true;

requiredFiles.forEach(file => {
  if (fs.existsSync(file)) {
    logSuccess(`${file} existe`);
  } else {
    logError(`${file} no encontrado`);
    allFilesExist = false;
  }
});

if (!allFilesExist) {
  logError('Faltan archivos requeridos del proyecto');
  process.exit(1);
}

// Verificar node_modules
console.log('\n📦 Verificando dependencias...');
if (fs.existsSync('node_modules')) {
  logSuccess('Carpeta node_modules existe');
  
  // Verificar algunas dependencias clave
  const keyDependencies = ['react', 'vite', '@vitejs/plugin-react-swc'];
  let allDepsExist = true;
  
  keyDependencies.forEach(dep => {
    if (fs.existsSync(`node_modules/${dep}`)) {
      logSuccess(`${dep} instalado`);
    } else {
      logError(`${dep} no encontrado en node_modules`);
      allDepsExist = false;
    }
  });
  
  if (!allDepsExist) {
    logWarning('Algunas dependencias faltan. Ejecuta: npm install --force');
  }
} else {
  logError('Carpeta node_modules no existe. Ejecuta: npm install');
  process.exit(1);
}

// Verificar que Vite funcione
console.log('\n⚡ Verificando Vite...');
try {
  execSync('npx vite --version', { encoding: 'utf8' });
  logSuccess('Vite está disponible');
} catch (error) {
  logError('Vite no está disponible. Ejecuta: npm install --force');
  process.exit(1);
}

// Verificar archivos JSON
console.log('\n📊 Verificando archivos de datos...');
try {
  const hotelsData = JSON.parse(fs.readFileSync('src/data/hotels.json', 'utf8'));
  const reviewsData = JSON.parse(fs.readFileSync('src/data/reviews.json', 'utf8'));
  const configData = JSON.parse(fs.readFileSync('src/data/config.json', 'utf8'));
  
  if (Array.isArray(hotelsData) && hotelsData.length > 0) {
    logSuccess(`hotels.json contiene ${hotelsData.length} hoteles`);
  } else {
    logWarning('hotels.json está vacío o no es un array válido');
  }
  
  if (reviewsData.positive && reviewsData.negative && reviewsData.recent) {
    logSuccess('reviews.json tiene estructura correcta');
  } else {
    logWarning('reviews.json no tiene la estructura esperada');
  }
  
  if (configData.app && configData.scraping && configData.filters) {
    logSuccess('config.json tiene configuración completa');
  } else {
    logWarning('config.json no tiene todas las configuraciones necesarias');
  }
} catch (error) {
  logError('Error al leer archivos JSON: ' + error.message);
}

console.log('\n🎉 Verificación completada!');
console.log('\n📋 Para ejecutar la aplicación:');
console.log('   npm run dev');
console.log('\n📋 O si hay problemas:');
console.log('   npx vite');
console.log('\n🌐 La aplicación estará disponible en: http://localhost:3000');
console.log('\n📚 Para más información, consulta README.md');
