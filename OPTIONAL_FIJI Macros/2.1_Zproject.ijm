inputDir1 = getDirectory("Choose image directory! "); 
outputDir = getDirectory("Choose Output image directory! "); 
fileList1 = getFileList(inputDir1); 

for (i = 0; i < fileList1.length; i++) { 
  file1 = fileList1[i]; 
  open(inputDir1+file1); 
  id1 = getImageID(); 
  run("Z Project...", "start=92 stop=121 projection=[Max Intensity]");
  outName = File.getName(file1); 
  saveAs("Tiff", outputDir + "/" + outName);
  close();
  close();
} 