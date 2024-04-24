This is the installation files for a robot waterer that feeds from a rain barrel. Learn more at the youtube link here:

To set up your raspberry pi zero w

If you log in via ssh and it hangs, improve ssh response times with this command and then reboot: echo "IPQoS cs0 cs0" | sudo tee -a /etc/ssh/sshd_config

install git on your raspberry pi: sudo apt-get -y install git

clone this git repository to your pi home directory: git clone https://github.com/NathanBuildsDIY/water.git

Run initial setup: nohup sh rain/initial-setup.sh & Note - you can watch the output with: tail -f nohup.out

Connect to the new wifi hostpot called rain. Visit http://rain.local/run to control your watering robot. 

You can still ssh to the waterer (while connected to the rain wifi) via ssh or putty
