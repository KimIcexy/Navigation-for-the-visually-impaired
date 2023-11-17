# Navigation for the visually impaired

>**Prerequisites**:
- Install Python
- Install Node
- Install React Native CLI:
```bash
npm install -g react-native-cli
```
- Have an Android device (physical or virtual):
    - *Physical device:* plugging it in to your computer using a USB cable and following 2 beginning steps of the instructions [here](https://reactnative.dev/docs/running-on-device).
    - *Android Emulator:* Following instruction in [React Native CLI Quick start - Android development environment](https://reactnative.dev/docs/environment-setup).

## Step 1: Set up backend
**1. Create a virtual environment**
```bash
python -m venv venv
```

**2. Activate the virtual environment**

Using command line:
```bash
venv/Scripts/activate.bat
```
or using powershell:
```bash
venv/Scripts/activate.ps1
```

**3. Install the packages**
```bash
pip install -r requirements.txt
```

**4. Start backend**
```bash
python app.py
```

## Step 2: Set up frontend
**1. Install the packages**
```bash
npm i
```

**2. Connect to an Android device (real or virtual)**
```bash
npx react-native run-android
```