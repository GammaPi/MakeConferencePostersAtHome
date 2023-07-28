# MakePostersAtHome

A tool to help you make conference posters out of home printers. Specifically, it automatically slices large-size PDF posters into smaller ones printable by your home printer. You need to follow guides on the smaller prints to stitch them together (check [sampleinput.pptx](sampleInput.pptx) and [output.pdf](output.pdf)). This tool was originally used in CV670 @ UMASS.

## Step1: Install this repo
1. git clone https://github.com/GammaPi/MakeConferencePostersAtHome.git
2. cd MakeConferencePostersAtHome
3. pip install -r requirements.txt

## Step2: Install poppler

Poppler is the underlying project that does the magic in pdf2image. You can check if you already have it installed by calling `pdftoppm -h` in your terminal/cmd.

**Ubuntu**

`sudo apt-get install poppler-utils`

**Archlinux**

`sudo pacman -S poppler`

**MacOS**

`brew install poppler`

**Windows**

1. Download the latest poppler package from [@oschwartz10612 version](https://github.com/oschwartz10612/poppler-windows/releases/) which is the most up-to-date.
2. Move the extracted directory to the desired place on your system
3. Add the `bin/` directory to your [PATH](https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/)
4. Test that all went well by opening `cmd` and making sure that you can call `pdftoppm -h`


## Step3: Make your poster
The process is simple:
1. The poster size depends on the PDF size. You can make a poster with PowerPoint and set the slide size to your desired size.
2. Export slides to PDF (Any PDF with your desired size will work)
3. Use Python to run this script `python3 main.py`  and generate the output PDF
4. Check and then use a printer to print the output.pdf (Each page from the input file will have one output PDF file.)
6. Cut/Fold the dark-grey edge, and put glue on the light-gray edge.
7. Stitch poster together.

There are a few input parameters (Note: Poster size is determined by your PDF settings)
```
<Absolute path to PDF file>
<Print Paper Width in inches>
<Print Paper Height in inches>
<Glue Border Width in inches>
```

Example generated image:

> Image courtesy: [Unsplash - Boston Public Library](https://unsplash.com/photos/_f9cP4_unmg)
![image](https://user-images.githubusercontent.com/19838874/206938666-b799a690-3e83-4b49-ad79-2610ec287bd7.png)

Folded paper (without glue this time):

![image](https://user-images.githubusercontent.com/19838874/206938781-a417feb7-a480-4e51-b477-55f25a723779.png)

Stitched poster:

![image](https://user-images.githubusercontent.com/19838874/206939046-cfc54152-f871-49c8-ab74-1c439dc46503.png)
