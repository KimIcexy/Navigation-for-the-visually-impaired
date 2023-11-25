# Predict depth image from RGB image
### Set up: 
Download the checkpoints using `rgb2depth/checkpoints/fetch_checkpoints.sh`:
```bash
cd backend/modules/obstacles/navigate/rgb2depth/checkpoints
bash ./fetch_checkpoints.sh
```

### Run:
Run `rgb2depth/predict.py` file:
```bash
cd .. 
python predict.py
```