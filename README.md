Mitsubishi RM501

Useful Links:

-[Forward Kinematics Move Master II](http://vlabs.iitkgp.ac.in/mr/exp2/index.html)

![RM 501 Robot](https://www.tuebingen.de/fotos/cache/stadtmuseum-roboter/industrieroboter_mitsubishi_2000_1920.jpg)


# Notes

- To calibrate run `robot_Lib/roboclaw_python_library_roboclaw/roboclaw_python/calibrate_arm_v2.py`. 

- To run mini-app (in robot_Lib/roboclaw_python_library_roboclaw/roboclaw_python/) folder run `streamlit run app.py`. Launches UI to control motor positions, wrist positions and gripper. 


echo "# RM501_Pi" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin git@github.com:diegopenilla/RM501_Pi.git
git push -u origin main