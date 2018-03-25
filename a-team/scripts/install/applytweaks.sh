sudo cp 01-notary.conf /etc/sysctl.d/
echo "tcp_bbr" | sudo tee --append /etc/modules-load.d/modules.conf
echo "* soft nofile 1000000" | sudo tee --append /etc/security/limits.conf
echo "* hard nofile 1000000" | sudo tee --append /etc/security/limits.conf
echo "session required pam_limits.so" | sudo tee --append /etc/pam.d/common-session 
