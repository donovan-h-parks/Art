import processing.core.*; 
import processing.xml.*; 

import controlP5.*; 

import java.applet.*; 
import java.awt.Dimension; 
import java.awt.Frame; 
import java.awt.event.MouseEvent; 
import java.awt.event.KeyEvent; 
import java.awt.event.FocusEvent; 
import java.awt.Image; 
import java.io.*; 
import java.net.*; 
import java.text.*; 
import java.util.*; 
import java.util.zip.*; 
import java.util.regex.*; 

public class ThePaintersScreensaver extends PApplet {

// The Painters
//
// Donovan Parks (donovan.parks@gmail.com)
// Feb., 2012


ControlP5 gControlP5;

String gImageFile = "AkakaFallsBamboo.jpg";
PImage gImage;

int gNumPainters = 1000;
float gBlendingFactor = 0.05f;
int gFrameRate = 90;

int gAppletWidth = 1600;
int gAppletHeight = 800;
int gMaxImageWidth = gAppletWidth-100;
int gMaxImageHeight = gAppletHeight-100;
int gControlHeight = 0;

int gInitImageDelay = 3;  // in seconds

Painter[] gPainters;
int gNumPaintersController = gNumPainters;

int gBackgroundColor = color(255, 255, 255);

int gFrameSize = 10;
int gImageOffsetX = 0;
int gImageOffsetY = 0;

File[] gFiles;
int gCurFileIndex = 0;

long gStartTime;

public void setup()
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
    
  resetAll();
}

public void resetAll()
{
  frameCount = 0;
  
  gBlendingFactor = random(0.0f, 0.1f);
  
  // load input image
  gImage = loadImage(gImageFile);
  if(gImage.width > gMaxImageWidth)
    gImage.resize(gMaxImageWidth, 0);
  if(gImage.height > gMaxImageHeight)
    gImage.resize(0, gMaxImageHeight);
    
  gImageOffsetX = PApplet.parseInt(0.5f*(gAppletWidth-gImage.width));
  gImageOffsetY = PApplet.parseInt(0.5f*(gAppletHeight-gControlHeight-gImage.height));
    
  gImage.loadPixels();
  
  // draw background, frame, and controls
  background(gBackgroundColor);
  
  stroke(192);
  fill(gBackgroundColor);
  rect(gImageOffsetX-gFrameSize, gImageOffsetY-gFrameSize, gImage.width + 2*gFrameSize, gImage.height + 2*gFrameSize);
  
  stroke(128);
  fill(128);
  rect(0, gAppletHeight-gControlHeight, gAppletWidth, gControlHeight);
  
  loadPixels();
    
  // initialize painters  
  gNumPainters = gNumPaintersController;
  gPainters = new Painter[gNumPainters];
  
  for(int i = 0; i < gNumPainters; ++i)
    gPainters[i] = new Painter();
    
  gStartTime = new Date().getTime(); //start time
}

public void draw()
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
  
  if(difference > 30000)
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

public File[] listFiles(String dir) 
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

public void keyPressed()
{
  if(keyCode == ENTER)
    saveImage();
}

public void addControls()
{
  int offsetX = gAppletWidth - gControlHeight + 10;
  int offsetY = PApplet.parseInt(0.5f*(gAppletHeight - 375));
  
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
  Slider blendingSlider = gControlP5.addSlider("blendingFactorChanged",0.00f,0.5f,gBlendingFactor,offsetY+110,offsetX+10,100,15);
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
  int gBrushColor;
  int gPainterStyle;  // 0 = grayscale, 1 = color
  
  Painter()
  { 
    regeneratePainter();
  }
  
  public void regeneratePainter()
  {
    gPosX = PApplet.parseInt(random(0, gImage.width-1));
    gPosY = PApplet.parseInt(random(0, gImage.height-1));
    gDir = PApplet.parseInt(random(0, 4));
    
    gPainterType = PApplet.parseInt(random(0, 5));
    if(gPainterType == 0 || gPainterType == 1)
      gPainterType = -1;
    else if(gPainterType == 2 || gPainterType == 3)
      gPainterType = 1;
    else if(gPainterType == 4)
      gPainterType = 0;
      
    gPainterType = 0;
      
    gPainterStyle = PApplet.parseInt(random(0, 2));
    
    gBrushColor = getColor(gPosX, gPosY);
    paintPixel(gPosX, gPosY);   
  }
  
  public int getColor(int x, int y)
  {
    int imageIndex = x + y*gImage.width;
    int pixelColor = gImage.pixels[imageIndex];
    
    //if(gPainterStyle == 0)
    //  pixelColor = color(brightness(pixelColor));
      
    return pixelColor;
  }
  
  public void paintPixel(int x, int y)
  {
    int pixelColor = getColor(x,y);    
    gBrushColor = lerpColor(gBrushColor, pixelColor, gBlendingFactor); 
    
    int canvasIndex = (x+gImageOffsetX) + (y+gImageOffsetY)*gAppletWidth;
    
    if(pixels[canvasIndex] == gBackgroundColor)
    {
      // Only paint on the empty canvas. This check is needed to control
      // regenerated painters.
      pixels[canvasIndex] = gBrushColor;
    }
  }
  
  public int nextPosX(int x, int dir)
  {
     if(dir == 1)
      x += 1;
    else if(dir == 3)
      x -= 1; 
      
    return x;
  }
  
  public int nextPosY(int y, int dir)
  {
     if(dir == 0)
      y -= 1;
    else if(dir == 2)
      y += 1; 
      
    return y;
  }
  
  public int nextDir(int dir, int painterType)
  {
    dir += painterType;
    if(dir < 0)
      dir = 3;
    else if(dir > 3)
      dir = 0;  
      
    return dir;
  }
  
  public boolean validMove(int x, int y)
  {
    if(x >= 0 && x < gImage.width && 
        y >= 0 && y < gImage.height)
    {
      int canvasIndex = (x+gImageOffsetX) + (y+gImageOffsetY)*gAppletWidth;
      int c = pixels[canvasIndex];
      if(c == gBackgroundColor)
        return true;
    }
    
    return false;
  }
  
  public void move()
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
  static public void main(String args[]) {
    PApplet.main(new String[] { "--present", "--bgcolor=#666666", "--hide-stop", "ThePaintersScreensaver" });
  }
}
