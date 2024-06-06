uniform vec2 u_resolution;
uniform vec2 u_mouse;
uniform float zoom;
uniform vec2 p;

void main() {
    vec2 c = p + zoom * (2.*gl_FragCoord.xy-u_resolution.xy)/u_resolution.y;

	vec2 z = c;

	float ar = 0.; // average of reciprocals
	float i;
	for (i = 0.; i < 50.; i++) {
		ar += 1./length(z);
		z = vec2(z.x * z.x - z.y * z.y, 2.0 * z.x * z.y) + c;
	}
	ar = ar / i;

	gl_FragColor = vec4(0.0, vec2(1.0 - (1. / ar)), ar / 2.0);
}
