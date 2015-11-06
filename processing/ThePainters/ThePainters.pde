// The Painters
//
// Donovan Parks (donovan.parks@gmail.com)
// Feb., 2012

import controlP5.*;
ControlP5 gControlP5;

String gImageFile = "AkakaFallsBamboo.jpg";
PImage gImage;

int gNumPainters = 250;
float gBlendingFactor = 0.05;
int gFrameRate = 120;

int gAppletSize = 900;
int gMaxImageDim = 840;
int gControlHeight = 40;

int gInitImageDelay = 2;  // in seconds

Painter[] gPainters;
int gNumPaintersController = gNumPainters;

color gBackgroundColor = color(255, 255, 255);

int gFrameSize = 10;
int gImageOffsetX = 0;
int gImageOffsetY = 0;

void setup()
{    
  gControlP5 = new ControlP5(this);
  
  size(gAppletSize, gAppletSize);
  addControls();
    
  resetAll();
}

public void resetAll()
{
  frameCount = 0;
  
  // load input image
  gImage = loadImage(gImageFile);
  if(gImage.width > gImage.height)
    gImage.resize(gMaxImageDim, 0);
  else
    gImage.resize(0, gMaxImageDim);
    
  gImageOffsetX = int(0.5*(gAppletSize-gImage.width));
  gImageOffsetY = int(0.5*(gAppletSize-gControlHeight-gImage.height));
    
  gImage.loadPixels();
  
  // draw background, frame, and controls
  background(gBackgroundColor);
  
  stroke(192);
  fill(gBackgroundColor);
  rect(gImageOffsetX-gFrameSize, gImageOffsetY-gFrameSize, gImage.width + 2*gFrameSize, gImage.height + 2*gFrameSize);
  
  stroke(128);
  fill(128);
  rect(0, gAppletSize-gControlHeight, gAppletSize, gControlHeight);
  
  loadPixels();
    
  // initialize painters  
  gNumPainters = gNumPaintersController;
  gPainters = new Painter[gNumPainters];
  
  for(int i = 0; i < gNumPainters; ++i)
    gPainters[i] = new Painter();
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
}

void keyPressed()
{
  if(keyCode == ENTER)
    saveImage();
}

void addControls()
{
  int offsetX = gAppletSize - gControlHeight + 10;
  int offsetY = int(0.5*(gAppletSize - 375));
  
  // Button to select image
  Button selectImageButton = gControlP5.addButton("selectImage",0,10,offsetX+10,65,15);
  selectImageButton.setLabel("Select Image");
  selectImageButton.activateBy(ControlP5.PRESSED);
  
  // Slider for number of painters
  Textlabel painterLabel = gControlP5.addTextlabel("painterLabel","painters:",offsetY,offsetX);
  Slider painterSlider = gControlP5.addSlider("numPaintersChanged",1,500,gNumPainters,offsetY,offsetX+10,100,15);
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
  Button saveImageButton = gControlP5.addButton("saveImage",0,gAppletSize-10-55,offsetX+10,55,15);
  saveImageButton.setLabel("Save image");
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
  int gPosX;
  int gPosY;
  int gDir; // 0 = North, 1 = East, 2 = South, 3 = West
  int gPainterType; // -1 = CCW, 0 = Straight, 1 = CW
  color gBrushColor;
  int gPainterStyle;  // 0 = grayscale, 1 = color
  
  Painter()
  { 
    regeneratePainter();
  }
  
  void regeneratePainter()
  {
    gPosX = int(random(0, gImage.width-1));
    gPosY = int(random(0, gImage.height-1));
    gDir = int(random(0, 4));
    
    gPainterType = int(random(0, 5));
    if(gPainterType == 0 || gPainterType == 1)
      gPainterType = -1;
    else if(gPainterType == 2 || gPainterType == 3)
      gPainterType = 1;
    else if(gPainterType == 4)
      gPainterType = 0;
      
    gPainterType = 0;
      
    gPainterStyle = int(random(0, 2));
    
    gBrushColor = getColor(gPosX, gPosY);
    paintPixel(gPosX, gPosY);   
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
    
    int canvasIndex = (x+gImageOffsetX) + (y+gImageOffsetY)*gAppletSize;
    
    if(pixels[canvasIndex] == gBackgroundColor)
    {
      // Only paint on the empty canvas. This check is needed to control
      // regenerated painters.
      pixels[canvasIndex] = gBrushColor;
    }
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
      int canvasIndex = (x+gImageOffsetX) + (y+gImageOffsetY)*gAppletSize;
      color c = pixels[canvasIndex];
      if(c == gBackgroundColor)
        return true;
    }
    
    return false;
  }
  
  void move()
  {  
    // can the painter make a valid right or left turn
    // depending on the type of painter
    int newDir = nextDir(gDir, gPainterType);  
    int newX = nextPosX(gPosX, newDir);
    int newY = nextPosY(gPosY, newDir);
      
    boolean bValidMove = validMove(newX, newY);
    if(bValidMove)
    {
      gPosX = newX;
      gPosY = newY;
      gDir = newDir;
    }
    
    // if not, go straight
    if(!bValidMove)
    {
      newX = nextPosX(gPosX, gDir);
      newY = nextPosY(gPosY, gDir);
      
      bValidMove = validMove(newX, newY);
      if(bValidMove)
      {
        gPosX = newX;
        gPosY = newY;
      }
    }
    
    // if not, check for any valid move
    if(!bValidMove)
    {
      newDir = gDir;
      for(int i = 0; i < 4; ++ i)
      {
        if(gPainterType == 0)
        {
          newDir = nextDir(newDir, 1); 
        }
        else
          newDir = nextDir(newDir, gPainterType); 
          
        newX = nextPosX(gPosX, newDir);
        newY = nextPosY(gPosY, newDir);
        
        bValidMove = validMove(newX, newY);
        if(bValidMove)
        {    
          gPosX = newX;
          gPosY = newY;
          gDir = newDir;
          break;
        }
      }
    }
    
    // paint pixel
    if(bValidMove)
      paintPixel(gPosX, gPosY);
    else
    {
      // if there are no valid moves, regenerate painter at a random location
      regeneratePainter();
    }    
  }
}
