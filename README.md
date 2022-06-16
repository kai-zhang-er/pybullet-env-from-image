# pybullet-env-from-image
Build simple pybullet environment from binary image
The core code is from [adaptive-box](https://github.com/jnfran92/adaptive-boxes). I make some simplification of the code and add the interface to convert directly from binary image


# How to use
change the image path in `test.py` and filter threshold to generate satisfied number of rectangles
```python
python test.py
```
With the generated `rect.txt`, run 
```python
python generate_env_from_txt.py
```
to build the pybullet 3D environment. Adjust the camera position and view angle to find the suitable view.

# Result
## input image
<img src="./floor_plan_simple.png" alt="sample1">

## output rectangle
<img src="./rect_result.png" alt="sample1">

## pybullet env
<img src="./pybullet_env_result.png" alt="sample1">

# to do list
- decompose rectangles from binary image
- draw boxes in pybullet according to rectangle info
