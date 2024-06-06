/*
 * animation.js
 * Copyright (C) 2022 Christopher Odom <christopher.r.odom@gmail.com>
 *
 * Distributed under terms of the MIT license.
 */
/*
 * Starts up the 3js library
 */

import * as THREE from 'three'
import { Power2 } from 'gsap'; // For smooth interpolation

var container;
var camera, scene, renderer, clock;
var uniforms;

var frag_shdr;
var vert_shdr;

fetch("/frag.glsl").then((response) => {
	return response.text();
}).then((in_frag_shdr) => {
	frag_shdr = in_frag_shdr;
}).then(() => {
	return fetch("/vert.glsl")
}).then((response) => {
	return response.text()
}).then((in_vert_shdr) => {
	vert_shdr = in_vert_shdr;
	init();
	animate();
}).catch((e) => {
	console.log(e)
})


function init() {
	container = document.getElementById( 'animContainer' );

	camera = new THREE.Camera();
	camera.position.z = 1;

	scene = new THREE.Scene();
	clock = new THREE.Clock();

	var geometry = new THREE.PlaneGeometry( 2, 2 );

  /* In my initializer */
  uniforms = {
      u_resolution: { type: "v2", value: new THREE.Vector2() },
      u_mouse: { type: "v2", value: new THREE.Vector2() },
      zoom: { type: "f", value: 1.0 },
      p: { type: "v2", value: new THREE.Vector2(-1.4108866282582646, 0.0) }
  };

	var material = new THREE.ShaderMaterial( {
		uniforms: uniforms,
		vertexShader:   vert_shdr, 
		fragmentShader: frag_shdr
	} );

	var mesh = new THREE.Mesh( geometry, material );
	scene.add( mesh );

	renderer = new THREE.WebGLRenderer();
	renderer.setPixelRatio( window.devicePixelRatio );
	renderer.setClearColor(0xffffff, 1);

	container.appendChild( renderer.domElement );

	onWindowResize();
	window.addEventListener( 'resize', onWindowResize, false );

	document.onmousemove = function(e){
		uniforms.u_mouse.value.x = e.pageX
		uniforms.u_mouse.value.y = e.pageY
	}
}

function onWindowResize( event ) {
	renderer.setSize( window.innerWidth, window.innerHeight );
	uniforms.u_resolution.value.x = renderer.domElement.width;
	uniforms.u_resolution.value.y = renderer.domElement.height;
	uniforms.u_resolution.value.z = 1;
}

function animate() {
	requestAnimationFrame( animate );
	render();
}

// Define keyframes
const keyframes = {
  '/': {
    zoom: 1.0 / (2.0),
    p: new THREE.Vector2(-1.25, 0.0)
  },
  '/blog': {
    zoom: 1.0 / (25.0),
    p: new THREE.Vector2(-1.4108866282582646, 0.0)
  }
  // Add more keyframes for other endpoints...
};

// Current animation target
let targetKeyframe = keyframes['/'];
let lastKeyframe = keyframes['/'];

// Function to interpolate between keyframes
function interpolateKeyframes(from, to, progress) {
  uniforms.zoom.value = from.zoom + (to.zoom - from.zoom) * progress;
  uniforms.p.value.x = from.p.x + (to.p.x - from.p.x) * progress;
  uniforms.p.value.y = from.p.y + (to.p.y - from.p.y) * progress;
}

let animationProgress = 0;
let animationStartTime = 0;

// Update animation in render loop
function render() {
  const currentTime = performance.now();
  const animationDuration = 1000; // 1 second

  // Calculate animation progress
  animationProgress = (currentTime - animationStartTime) / animationDuration;
  animationProgress = Math.min(animationProgress, 1); // Clamp to [0, 1]

  // Interpolate keyframes
  const currentKeyframe = {
    zoom: uniforms.zoom.value,
    p: uniforms.p.value.clone()
  };
  interpolateKeyframes(currentKeyframe, targetKeyframe, Power2.easeInOut(animationProgress));

  // Render scene
  renderer.render(scene, camera);
}

export function animateRouteChange(to, from) {
  lastKeyframe = targetKeyframe;
  targetKeyframe = keyframes[to.path.toLowerCase()];
  const currentKeyframe = lastKeyframe;

  // Reset animation progress
  animationProgress = 0;
  animationStartTime = performance.now();
}

