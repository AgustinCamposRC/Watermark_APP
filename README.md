# Watermark_App
An image watermark apps created in python that that allows you to add a custom watermark image or text in a base img and save it in the chosen directory.The application use ttkbootstrap, matplotlib and Pillow libraries to create all app features.

## GUI Layout
The GUI application is made up of several components, among them, frames, buttons, labels, combobox, Scales, Entrys, which allow the interaction with the user. With these elements the user can customize the characteristics of the watermark, such as font type, size, color, opacity, content and position.

![image](https://github.com/AgustinCamposRC/Watermark_App/assets/130417572/bc3ec4a0-6524-418d-946a-4185e1b7b3ab)

## Creation and Customization of Watermarks
The application allows the user to create between a watermark image and a watermark text, furthermore the user has the ability to customize the watermark by providing the text or image to be transformed into a watermark. You can adjust the watermark position, rotation, font size, font type, opacity and color using the various components of the graphical user interface. In the process, the app converts the image file into RGB to save it later.

![image](https://github.com/AgustinCamposRC/Watermark_App/assets/130417572/7ddc48a4-3265-48e7-8fd6-1344494f9247)


![image](https://github.com/AgustinCamposRC/Watermark_App/assets/130417572/d4553e3b-3c1f-4f50-9690-e317fe2808ea)


![image](https://github.com/AgustinCamposRC/Watermark_App/assets/130417572/ffe27fe5-f97f-4ec3-8208-62bfa34bb6c0)


![image](https://github.com/AgustinCamposRC/Watermark_App/assets/130417572/4f27fc61-ea03-4945-82be-1f93810af116)


## Saving Process
Once you have customized your watermark, you can save the new image with the watermark by clicking the "Save" button. This allows you to name your watermarked image and save it in the chosen file path. The initial name of the new image is the same as that of the base image.

![image](https://github.com/AgustinCamposRC/Watermark_App/assets/130417572/6efd8ca4-b7e2-4d6c-ba19-f5e53dd48f24)

## Installation
1. Clone the repository: 
```
https://github.com/AgustinCamposRC/Watermark_App.git
```
2. Change directory into the project folder
3. Create virtual environment: 
```
python -m venv venv
``` 
```
venv/Scripts/activate
```
4. Install the required packages: 
```
pip install -r requirements.txt
```
5. Run the `main.py`

## Dependencies

Libraries Used:

✅ Tkinter
✅ ttkbootstrap
✅ Pillow
✅ Matplotlib
