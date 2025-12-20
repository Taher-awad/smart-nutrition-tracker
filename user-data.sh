#!/bin/bash
# Add 2GB Swap for Flutter Build
dd if=/dev/zero of=/swapfile bs=128M count=16
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile

# Install Docker
yum update -y
amazon-linux-extras install docker -y
service docker start
usermod -a -G docker ec2-user

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Git & Deploy
yum install git -y
cd /home/ec2-user
git clone https://github.com/Taher-awad/smart-nutrition-tracker.git
cd smart-nutrition-tracker

# Start App
docker-compose up -d
