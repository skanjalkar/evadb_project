# awsWebsite
My naive implementation and learning project of JavaScript and nodejs

Before running the code, redirect port 3000 to port 80 by running the following in the cloud:
```
sudo iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 3000
```
