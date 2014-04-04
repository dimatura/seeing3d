
varying vec3 vertex_color;

void main()
{
    gl_FragColor = vec4(vertex_color, 1.0);
}

