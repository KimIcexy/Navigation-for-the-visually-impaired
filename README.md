# Navigation for the visually impaired

> **Prerequisites**:

-   Install Python
-   Install Node
-   Install React Native CLI:

```bash
npm install -g react-native-cli
```

-   Have an Android device (physical or virtual):
    -   _Physical device:_ plugging it in to your computer using a USB cable and following 2 beginning steps of the instructions [here](https://reactnative.dev/docs/running-on-device).
    -   _Android Emulator:_ Following instruction in [React Native CLI Quick start - Android development environment](https://reactnative.dev/docs/environment-setup).

## Step 1: Set up backend

**1. Create a virtual environment**

```bash
python -m venv venv
```

**2. Activate the virtual environment**

Using command line:

```bash
backend\venv\Scripts\activate.bat
```

or using powershell:

```bash
backend\venv\Scripts\Activate.ps1
```

**3. Install the packages**

```bash
pip install -r requirements.txt
```

**4. Start backend**

```bash
python app.py
```

**5. Start ngrok**

```bash
ngrok http --region jp ${PORT}
```

## Step 2: Set up frontend

**1. Install the packages**

```bash
npm install
```

or

```bash
yarn install
```

**2. Connect to an Android device (real or virtual)**

```bash
npx run start
```

or

```bash
yarn run start
```

**3. Run on Android device**

```bash
npx run android
```

or

```bash
yarn run android
```

## About us:

-   Huynh Thiet Gia: 20120070
-   Nguyen Duy Quang: 20120360
-   Dang Vo Hoang Kim Tuyen: 20120399
