import { Application } from 'https://unpkg.com/@splinetool/runtime@latest/build/runtime.js';

const canvas = document.getElementById('canvas3d');
const app = new Application(canvas);
app.load('https://prod.spline.design/3FR08zFELjCpKvPw/scene.splinecode');
