# apkutil

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/aktsk/apkutil/blob/master/LICENSE)

`apkutil` is a useful utility for mobile security testing.
It is a wrapper for `apktool` and `apksigner`, `aapt` commands.
I've only checked it works on macOS.

## Requirements

- Android SDK build tools
- [Apktool](https://ibotpeaches.github.io/Apktool/)

Also, place `~/apkutil.json` containing the keystore information necessary for signing apk in your home directory.

```
{
    "keystore_path": "hoge.keystore",
    "ks-key-alias": "fuga",
    "ks-pass": "pass:foo"
}
```

## Installation
Since `apkutil` is implemented in Python, it can be installed with the pip command, which is a Python package management system.

```
$ pip install git+ssh://git@github.com/aktsk/apkutil.git
```

## Usage
The command outputs are displayed in color. You can use a function with subcommands.
The GIF is a scene of changing the APK to debuggable.

![debuggable](./img/debuggable.gif)

### subcommands
Most of the subcommands are assigned with alias, which is useful.

|subcommand  |alias  |desc  |
|---|---|---|
|`debuggable` |`debug`, `dg`  | make APK debuggable  |
|`info` | `i` | identify the package name |
|`screenshot` |`ss`  |get screenshot from connected device |
|`decode` |`d`  |decode APK |
|`build` |`b`  |build APK |
|`sign` |`s`  |sign APK |


### debuggable
`debuggable` subcommand makes the APK debuggable.
Decode the APK, set debuggable attribute to `true` in AndroidManifest, and rebuild it.
This feature is useful to use [aktsk/apk-medit](https://github.com/aktsk/apk-medit).


```
$ apkutil debuggable sample.apk
Decoding APK by Apktool...
I: Using Apktool 2.4.1 on sample.apk
I: Loading resource table...
I: Decoding AndroidManifest.xml with resources...
I: Loading resource table from file: /Users/taichi.kotake/Library/apktool/framework/1.apk
I: Regular manifest package...
I: Decoding file-resources...
I: Decoding values */* XMLs...
I: Baksmaling classes.dex...
I: Copying assets and libs...
I: Copying unknown files...
I: Copying original files...

Checking AndroidManifest.xml...
Permission:
android.permission.INTERNET

Debuggable:
False

AllowBackup:
False

Set debuggable attribute to true in AndroidManifest!

Building APK by Apktool...
I: Using Apktool 2.4.1
I: Checking whether sources has changed...
I: Smaling smali folder into classes.dex...
I: Checking whether resources has changed...
I: Building resources...
I: Copying libs... (/lib)
I: Building apk file...
I: Copying unknown files/dir...
I: Built apk...

Signing APK by apksigner...
Signed

Output: sample.patched.apk
```

### info
`info` subcommand allows you to see the package name.

```
$ apkutil info sample.apk
Getting package name by aapt...
    A: package="jp.aktsk.sample" (Raw: "jp.aktsk.sample")
```

### screenshot
`screenshot` subcommand allows you to get screenshot from connected device.

```
$ apkutil screenshot 
Getting a screenshot from connected device...
/data/local/tmp/screenshot-2020-05-21-16-58-20.png: 1 file pulled. 2.1 MB/s (14419 bytes in 0.007s)

Output: screenshot-2020-05-21-16-58-20.png
```

### decode
`decode` subcommand make the APK decode by apktool.

```
$ apkutil decode sample.apk
Decoding APK by Apktool...
I: Using Apktool 2.4.1 on sample.apk
I: Loading resource table...
I: Decoding AndroidManifest.xml with resources...
I: Loading resource table from file: /Users/taichi.kotake/Library/apktool/framework/1.apk
I: Regular manifest package...
I: Decoding file-resources...
I: Decoding values */* XMLs...
I: Baksmaling classes.dex...
I: Copying assets and libs...
I: Copying unknown files...
I: Copying original files...

Checking AndroidManifest.xml...
Permission:
android.permission.INTERNET

Debuggable:
False

AllowBackup:
False
```

### build
`build` subcommand make the APK build by apktool.
It also sign the APK after the build is complete.

```
$ apkutil build sample
Building APK by Apktool...
I: Using Apktool 2.4.1
I: Checking whether sources has changed...
I: Smaling smali folder into classes.dex...
I: Checking whether resources has changed...
I: Building resources...
I: Copying libs... (/lib)
I: Building apk file...
I: Copying unknown files/dir...
I: Built apk...

Signing APK by apksigner...
Signed

Output: sample.patched.apk
```

### sign
`sign` subcommand make the apk sign by apksigner.

```
$ apkutil sign sample.apk
Signing APK by apksigner...
Signed
```

## License
MIT License
