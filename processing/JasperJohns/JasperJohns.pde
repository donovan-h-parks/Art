// Generate art in the style of Jasper John's
//  "Between the Clock and the Bed"
//
// Donovan Parks (donovan.parks@gmail.com)
// Feb., 2012

import controlP5.*;
ControlP5 gControlP5;

int gNumLineSets = 10;
float gBlendingFactor = 0.05;
int gFrameRate = 120;

int gCanvasSize = 900;
int gFrameSize = 10;
int gControlHeight = 40;

JasperJohn gJJ;

color gBackgroundColor = color(255, 255, 255);

void setup()
{    
  gControlP5 = new ControlP5(this);
  
  size(gCanvasSize, gCanvasSize + gControlHeight);
    
  gJJ = new JasperJohn();

  addControls();  
  resetAll();
}

public void resetAll()
{
  // draw background, frame, and controls
  background(gBackgroundColor);
  
  stroke(192);
  fill(gBackgroundColor);
  rect(gFrameSize, gFrameSize, gCanvasSize - 2*gFrameSize, gCanvasSize - 2*gFrameSize);

  stroke(128);
  fill(128);
  rect(0, gCanvasSize, gCanvasSize, gControlHeight);
  
  gJJ.setNumLineSets(gNumLineSets);
  
  loadPixels();
}

void draw()
{ 
  gJJ.draw();
}

void keyPressed()
{
  if(keyCode == ENTER)
    saveImage();
}

void addControls()
{ 
  int offsetX = gFrameSize;
  int offsetY = gCanvasSize + gFrameSize;
  
  // Slider for number of line sets
  Textlabel lineSetsLabel = gControlP5.addTextlabel("lineSetsLabel","line sets:",offsetX,offsetY);
  Slider lineSetsSlider = gControlP5.addSlider("numLineSetsChanged",1,100,gNumLineSets,offsetX,offsetY+10,100,15);
  lineSetsSlider.setLabel("");
  
  // Slider for blending factor
  Textlabel blendingLabel = gControlP5.addTextlabel("blendingLabel","blending factor:",offsetX+110,offsetY);
  Slider blendingSlider = gControlP5.addSlider("blendingFactorChanged",0.00,0.5,gBlendingFactor,offsetX+110,offsetY+10,100,15);
  blendingSlider.setLabel("");
  
  // Slider for frame rate
  Textlabel frameRateLabel = gControlP5.addTextlabel("frameRateLabel","frame rate:",offsetX+220,offsetY);
  Slider frameRateSlider = gControlP5.addSlider("frameRateChanged",1,240,gFrameRate,offsetX+220,offsetY+10,100,15);
  frameRateSlider.setLabel("");
  
  // Button to redraw image
  Button redrawButton = gControlP5.addButton("resetAll",0,offsetX+330,offsetY+10,45,15);
  redrawButton.setLabel("Redraw");
  
  // Button to save image
  Button saveImageButton = gControlP5.addButton("saveImage",0,gCanvasSize-10-55,offsetY+10,55,15);
  saveImageButton.setLabel("Save image");
}

public void saveImage()
{
  String savePath = selectOutput();
  
  if(savePath != null)
  {
    PImage newImg = get(gFrameSize, gFrameSize, gCanvasSize - 2*gFrameSize, gCanvasSize - 2*gFrameSize);
    newImg.save(savePath);
  }
}

public void numLineSetsChanged(int lineSets)
{
  gNumLineSets = lineSets;
}

public void blendingFactorChanged(float blendingFactor)
{
  gBlendingFactor = blendingFactor;
}

public void frameRateChanged(int frameRate)
{
  gFrameRate = frameRate;
}

// JasperJohn ------------------------------------------------

class JasperJohn {
  int gNumLineSets;
  LineSets gLineSets;
  
  JasperJohn()
  { 
    init();
  }
  
  void init()
  {

  }
  
  void setNumLineSets(int numLineSets)
  {
    gNumLineSets = numLineSets;
  }
  
  void draw()
  {
    
  }
}

// LineSets ------------------------------------------------

class LineSets {
  int gNumLines = 0;
  
  LineSets()
  { 
    init();
  }
  
  void init()
  {
    gNumLines = 0;
  }
}

// Line ------------------------------------------------

class MyLine {
  float gStartX;
  float gStartY;
  
  float gEndX1;
  float gEndY1;
  
  float gEndX2;
  float gEndY2;
  
  float gAngle;
  float xStep;
  float yStep;
  
  color gColor;
  
  MyLine(int startX, int startY, float angle, color c)
  { 
    gStartX = gEndX1 = gEndX2 = startX;
    gStartY = gEndY1 = gEndY2 = startY;
    
    gAngle = angle;
    xStep = cos(angle);
    yStep = sin(angle);
    
    gColor = c;
  }
  
  void growLine()
  {
    gEndX1 += xStep;
    gEndY1 += yStep;
    
    gEndX2 -= xStep;
    gEndY2 -= yStep;
    
    
  }
}
