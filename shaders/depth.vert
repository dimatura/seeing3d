varying vec3 vertex_color;
void main()
{
    gl_Position = ftransform();
    vec4 vect = gl_ModelViewMatrix * gl_Vertex;
    vect = vect/vect.w;
    vertex_color = (vec3(-vect.z, -vect.z, -vect.z)-80.0)/45.0;
}
