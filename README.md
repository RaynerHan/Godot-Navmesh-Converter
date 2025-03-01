# Godot-Navmesh-Converter
Simple tool to convert Godot Navmeshes .tres into .obj or vise versa.

[![icon.png](https://i.postimg.cc/WpGZCbhw/icon.png)](https://postimg.cc/LhshZSkJ)

It is actually for personal use, but it would be better if I share it with the public and also keep it as a backup.

## Why did I make this?
I prefer to edit the navmesh on Blender and even optimize it using Meshlab or any polygon simplification algorithm so it won't make too much polygon, but I also really like to use Godot Bake Navmeshes and then convert to obj as a starting point for further edit.

## Can you use it for a project or any?
Yeah, I put it on the MIT license so you can use it for anything, for use it as I use it or fork it to make a better version than I create or somehow integrate it into Godot addons and Blender plugins, it all fine by me.

## Installation

Currently, it is only available on Windows, but if you know what you doing and wanna build it on other platforms, please do it.

### Method 1 "Build by your own"
1. Clone or Download all files
2. Make sure you install Python 3.13.2 or the latest
3. Then install pyinstaller by opening CMD.exe and typing `pip install pyinstaller`
4. After that run the build.bat
5. and you're done, you can start using the software like method 2 on part 

### Method 2 "Download and Run"
1. Download the release version of GodotNavmeshConverter.exe
2. after that drag and drop the obj. or .tres file to the GodotNavmeshConverter.exe
3. Wait and done

I might not gonna update this repo unless Godot updates how .tres works and breaks the compatibility or I find a bug. so like I said it is mostly for personal use but you are allowed to copy and use it for anything you want.
