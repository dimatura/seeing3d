varying vec3 vertex_color;
void main()
{

    gl_Position = ftransform();

    vertex_color = 0.5 + (gl_NormalMatrix * gl_Normal.xyz)/2.0;
}
