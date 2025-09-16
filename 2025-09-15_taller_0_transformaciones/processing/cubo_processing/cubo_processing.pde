void setup() {
  size(500, 500, P3D);
}

void draw() {
  background(0);
  translate(width/2, height/2);
  
  pushMatrix(); 
  
  //transformaciones
  translate(100 * sin(millis()/1000.0), 0); // traslacion
  rotateY(frameCount * 0.01); // rotacion
  scale(1 + sin(millis()/500.0) * 0.5); // escala
  
  box(80); // cubo
  popMatrix();
}
