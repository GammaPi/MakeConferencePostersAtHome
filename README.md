# MakePostersAtHome

This is a tool to make conference posters out of home printers. Specifically, it automatically generates images to print on a small piece of paper and helps you make a large poster with multiple papers by stitching them together. This tool is originally used in CV670 @ UMASS.

The process is simple:
Convert the poster to an image. (Pay attention to the DPI value. DPI should be consistent with your printer setting and the image setting if you want the exact poster size.)
Run my script, input the following parameters, and hit enter after each input. You might want to use a value smaller than the actual paper size as printers cannot print full paper size.
```
<Print Paper Width in inches>
<Print Paper Height in inches>
<Glue Border Width in inches>
<Printer DPI>
<Image Path>
```
The script will generate a series of images tagged with cutting hints.
Print the image with true size (no scaling).
Simply fold or cut away the gray edge, put glue on the white edge, and stick them together. You can adjust the glue border size is defined by yourself.


Example generated image:


> Image courtesy: [Unsplash - Boston Public Library](https://unsplash.com/photos/_f9cP4_unmg)
![image](https://user-images.githubusercontent.com/19838874/206938666-b799a690-3e83-4b49-ad79-2610ec287bd7.png)

Folded paper (without glue this time):

![image](https://user-images.githubusercontent.com/19838874/206938781-a417feb7-a480-4e51-b477-55f25a723779.png)

Stitched poster:

![image](https://user-images.githubusercontent.com/19838874/206938716-d273e9f9-125c-424a-9ecf-9ecbec6aa7c8.png)
