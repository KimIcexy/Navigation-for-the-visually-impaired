# Predict depth image from RGB image (~3 minutes)
### Set up: 
Download the checkpoints using `rgb2depth/checkpoints/fetch_checkpoints.sh`:
```bash
cd backend/modules/obstacles/navigate/rgb2depth/checkpoints
bash ./fetch_checkpoints.sh
```

### Run:
- Open a new window, activate the virtual environment.
- Run `rgb2depth/predict.py` file:
```bash
cd  backend/modules/obstacles/navigate/rgb2depth
python predict.py
```