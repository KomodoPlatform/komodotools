#Check if BBR Module is avalible
if [ "$(sudo modprobe tcp_bbr)" != "" ]
	then
	  echo "tcp_bbr Module not supported, install other network tweaks"
	  sudo cp 01-notary.conf /etc/sysctl.d/
	else
	  echo "tcp_bbr Module is supported, install it with network tweaks."
	  echo "net.ipv4.tcp_congestion_control=bbr" | tee --append 01-notary.conf
	  sudo cp 01-notary.conf /etc/sysctl.d/
      echo "tcp_bbr" | sudo tee --append /etc/modules-load.d/modules.conf
	fi
#Set the ulimit for open files for the user.	
echo "$USER soft nofile 1000000" | sudo tee --append /etc/security/limits.conf
echo "$USER hard nofile 1000000" | sudo tee --append /etc/security/limits.conf
echo "session required pam_limits.so" | sudo tee --append /etc/pam.d/common-session 
