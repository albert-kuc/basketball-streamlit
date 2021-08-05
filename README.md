# NBA player stats explorer
Stats explorer app displays NBA players stats per season. 
Players data is received from [Basketball-reference.com](https://www.basketball-reference.com/). <br>
Initial app idea and content is adapted from [Streamlit tutorial](https://youtu.be/xiBXspqs0dk) by 
[Data Professor](https://www.youtube.com/channel/UCV8e2g4IWQqK71bbzGDEI4Q)
tutorial.<br>
The final app expands with a few additional features learned by exploration.

### Launch online:
<a href="https://share.streamlit.io/albertkuc/basketball-streamlit/main/basketball_app.py" rel="nofollow">
    <img src="https://camo.githubusercontent.com/767be70c92254555bd347ab07908fec67854c2264b77702581bd230fd7eac54f/68747470733a2f2f7374617469632e73747265616d6c69742e696f2f6261646765732f73747265616d6c69745f62616467655f626c61636b5f77686974652e737667">
</a>

### Install
Create conda environment
```commandline
conda create --name basketball_env python=3.9.6
```
Switch to *basketball_env* environment
```commandline
conda activate basketball_env
```
Clone app repository
```commandline
git clone https://github.com/albertkuc/basketball-streamlit.git
```
Install required libraries and dependencies
```commandline
pip install -r requirements.txt
```