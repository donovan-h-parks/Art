// The Painters
//
// Donovan Parks (donovan.parks@gmail.com)
// Feb., 2012

import controlP5.*;
ControlP5 gControlP5;

String gImageFile = "HaleakalaSlidingSands.jpg";
PImage gImage;

int gNumPainters = 4000;
float gBlendingFactor = 0.08;
int gFrameRate = 240;

int gAppletWidth = 1920;
int gAppletHeight = 1080;
int gMaxImageWidth = gAppletWidth-500;
int gMaxImageHeight = gAppletHeight-400;
int gControlHeight = 0;

int gInitImageDelay = 3;  // in seconds

Painter[] gPainters;
int gNumPaintersController = gNumPainters;

color gBackgroundColor = color(0, 0, 0);

int gFrameSize = 10;
int gImageOffsetX = 0;
int gImageOffsetY = 0;

File[] gFiles;
int gCurFileIndex = 0;

long gStartTime;

void setup()
{    
  gControlP5 = new ControlP5(this);
  
  size(gAppletWidth, gAppletHeight);
  addControls();
  
  gFiles = listFiles(sketchPath);
  do
  {
    gCurFileIndex++;
  }
  while(!gFiles[gCurFileIndex].getName().contains("jpg"));
  gImageFile = gFiles[gCurFileIndex].getName();
  
  println(gImageFile);

  resetAll();
}

public void resetAll()
{
  frameCount = 0;
  
  // load input image
  gImage = loadImage(gImageFile);
  if(gImage.width > gMaxImageWidth)
    gImage.resize(gMaxImageWidth, 0);
  if(gImage.height > gMaxImageHeight)
    gImage.resize(0, gMaxImageHeight);
    
        
  gImageOffsetX = int(0.5*(gAppletWidth-gImage.width));
  gImageOffsetY = int(0.5*(gAppletHeight-gControlHeight-gImage.height));
    
  gImage.loadPixels();
  
  // draw background, frame, and controls
  background(gBackgroundColor);
  
  stroke(255);
  fill(gBackgroundColor);
  rect(gImageOffsetX-gFrameSize, gImageOffsetY-gFrameSize, gImage.width + 2*gFrameSize, gImage.height + 2*gFrameSize);
  
  stroke(128);
  fill(128);
  rect(0, gAppletWidth-gControlHeight, gAppletHeight, gControlHeight);
  
  loadPixels();
    
  // initialize painters  
  gNumPainters = gNumPaintersController;
  gPainters = new Painter[gNumPainters];
  
  for(int i = 0; i < gNumPainters; ++i)
    gPainters[i] = new Painter();
    
  gStartTime = new Date().getTime(); //start time
}

void draw()
{ 
  if(frameCount < gInitImageDelay)
  {
    image(gImage, gImageOffsetX, gImageOffsetY);
    frameRate(1);
  }
  else
  {  
    frameRate(gFrameRate);
    for(int i = 0; i < gNumPainters; ++i)
     gPainters[i].move();
    updatePixels();
  }
  
  long lEndTime = new Date().getTime(); //end time
  long difference = lEndTime - gStartTime; //check different
  
  if(difference > 60000)
  {
    do
    {
      gCurFileIndex++;
      if(gCurFileIndex > gFiles.length-1)
        gCurFileIndex = 0;
    }
    while(!gFiles[gCurFileIndex].getName().contains("jpg"));
    gImageFile = gFiles[gCurFileIndex].getName();
    resetAll();
  }
}

void keyPressed()
{
  if(keyCode == ENTER)
    saveImage();
}

void addControls()
{
  int offsetX = gAppletWidth - gControlHeight + 10;
  int offsetY = int(0.5*(gAppletHeight - 375));
  
  // Button to select image
  Button selectImageButton = gControlP5.addButton("selectImage",0,10,offsetX+10,65,15);
  selectImageButton.setLabel("Select Image");
  selectImageButton.activateBy(ControlP5.PRESSED);
  
  // Slider for number of painters
  Textlabel painterLabel = gControlP5.addTextlabel("painterLabel","painters:",offsetY,offsetX);
  Slider painterSlider = gControlP5.addSlider("numPaintersChanged",1,5000,gNumPainters,offsetY,offsetX+10,100,15);
  painterSlider.setLabel("");
  
  // Slider for blending factor
  Textlabel blendingLabel = gControlP5.addTextlabel("blendingLabel","blending factor:",offsetY+110,offsetX);
  Slider blendingSlider = gControlP5.addSlider("blendingFactorChanged",0.00,0.5,gBlendingFactor,offsetY+110,offsetX+10,100,15);
  blendingSlider.setLabel("");
  
  // Slider for frame rate
  Textlabel frameRateLabel = gControlP5.addTextlabel("frameRateLabel","frame rate:",offsetY+220,offsetX);
  Slider frameRateSlider = gControlP5.addSlider("frameRateChanged",1,240,gFrameRate,offsetY+220,offsetX+10,100,15);
  frameRateSlider.setLabel("");
  
  // Button to redraw image
  Button redrawButton = gControlP5.addButton("resetAll",0,offsetY+330,offsetX+10,45,15);
  redrawButton.setLabel("Redraw");
  
  // Button to save image
  Button saveImageButton = gControlP5.addButton("saveImage",0,gAppletHeight-10-55,offsetX+10,55,15);
  saveImageButton.setLabel("Save image");
}

File[] listFiles(String dir) 
{
  File file = new File(dir);
  if (file.isDirectory()) 
  {
    File[] files = file.listFiles();
    return files;
  } else {
    // If it's not a directory
    return null;
  }
}

public void selectImage(int theValue)
{
  String newImageFile = selectInput();
  if(newImageFile != null)
  {
    gImageFile = newImageFile;
    resetAll();
  }  
}

public void saveImage()
{
  String savePath = selectOutput();
  
  if(savePath != null)
  {
    PImage newImg = get(gImageOffsetX, gImageOffsetY, gImage.width, gImage.height);
    newImg.save(savePath);
  }
}

public void numPaintersChanged(int painters)
{
  gNumPaintersController = painters;
}

public void blendingFactorChanged(float blendingFactor)
{
  gBlendingFactor = blendingFactor;
}

public void frameRateChanged(int frameRate)
{
  gFrameRate = frameRate;
}

// Painter ------------------------------------------------

class Painter {
  float gPosX;
  float gPosY;
  int gDir; // 0 = North, 1 = East, 2 = South, 3 = West
  float gRadius;
  float gRad;
  int gPainterType; // -1 = CCW, 0 = Straight, 1 = CW
  color gBrushColor;
  int gPainterStyle;  // 0 = grayscale, 1 = color
  int gLifeSpan;
  
  Painter()
  { 
    regeneratePainter();
  }
  
  void regeneratePainter()
  {
    gPosX = int(random(0, gImage.width-1));
    gPosY = int(random(0, gImage.height-1));
    gDir = int(random(0, 4));
    gRadius = 1;
    gRad = random(0, 2*PI);
    gLifeSpan = 200;
    
    gPainterType = int(random(0, 5));
    if(gPainterType == 0 || gPainterType == 1)
      gPainterType = -1;
    else if(gPainterType == 2 || gPainterType == 3)
      gPainterType = 1;
    else if(gPainterType == 4)
      gPainterType = 0;
      
    gPainterType = 0;
      
    gPainterStyle = int(random(0, 2));
    
    gBrushColor = getColor(int(gPosX), int(gPosY));
    paintPixel(int(gPosX), int(gPosY));   
  }
  
  color getColor(int x, int y)
  {
    int imageIndex = x + y*gImage.width;
    color pixelColor = gImage.pixels[imageIndex];
    
    //if(gPainterStyle == 0)
    //  pixelColor = color(brightness(pixelColor));
      
    return pixelColor;
  }
  
  void paintPixel(int x, int y)
  {
    color pixelColor = getColor(x,y);    
    gBrushColor = lerpColor(gBrushColor, pixelColor, gBlendingFactor); 
    
    int canvasIndex = (x+gImageOffsetX) + (y+gImageOffsetY)*gAppletWidth;
    pixels[canvasIndex] = gBrushColor;
  }
  
  int nextPosX(int x, int dir)
  {
     if(dir == 1)
      x += 1;
    else if(dir == 3)
      x -= 1; 
      
    return x;
  }
  
  int nextPosY(int y, int dir)
  {
     if(dir == 0)
      y -= 1;
    else if(dir == 2)
      y += 1; 
      
    return y;
  }
  
  int nextDir(int dir, int painterType)
  {
    dir += painterType;
    if(dir < 0)
      dir = 3;
    else if(dir > 3)
      dir = 0;  
      
    return dir;
  }
  
  boolean validMove(int x, int y)
  {
    if(x >= 0 && x < gImage.width && 
        y >= 0 && y < gImage.height)
    {
      int canvasIndex = (x+gImageOffsetX) + (y+gImageOffsetY)*gAppletWidth;
      color c = pixels[canvasIndex];
      if(c == gBackgroundColor)
        return true;
    }
    
    return false;
  }
  
  void move()
  {  
    /*
    int x = int(gPosX + (gRadius*cos(gRad)));
    int y = int(gPosY + (gRadius*sin(gRad)));
    
    gRadius += 0.1;
    gRad += (2*PI) / 90;
    if(gRad > 2*PI)
      gRad -= 2*PI;
    
    if(gRadius > 25 || x < 0 || y < 0 || x >= gImage.width || y >= gImage.height)
      regeneratePainter();
    else
      paintPixel(x, y);   
   */
   
   gPosX += random(-2, 2);
   gPosY += random(-2, 2);
   
   gLifeSpan--;
   
    if(gLifeSpan < 0 || gPosX < 0 || gPosY < 0 || gPosX >= gImage.width || gPosY >= gImage.height)
      regeneratePainter();
    else
      paintPixel(int(gPosX), int(gPosY));
  }
}
