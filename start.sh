#!/bin/bash
apt-get update
apt-get install -y apache2
echo "<h1>Cloud Bursting Successful! Hello from GCP!</h1>" > /var/www/html/index.html
