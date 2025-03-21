import boto3
from time import sleep
import logging
from os import system

logging.basicConfig(
    level=logging.INFO,  # Set logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()  # Print logs to stdout (important for Docker)
    ]
)

# AWS Region
REGION = "ap-south-1"

# Nginx backend config file
frontend = set()
backend = set()

def fetch_instance_ips(name):
    ec2 = boto3.client("ec2", region_name=REGION)

    instances = ec2.describe_instances(
        Filters=[
            {"Name": "instance-state-name", "Values": ["running"]},
            {"Name": "tag:Name", "Values": [name]}
        ]
    )
    IP = set()
    for reservation in instances["Reservations"]:
        for instance in reservation["Instances"]:
            ip = instance["PrivateIpAddress"]
            IP.add(ip)
    return IP

def update_nginx_config(name, ips):
    if ips == set():
        ips = set(["127.0.0.1"])

    logging.info(f"Updating Nginx config with IPs: {list(ips)}")
    with open(f"/etc/nginx/conf.d/{name}s.conf", "w") as f:
        for ip in ips:
            f.writelines(f"server {ip}:5000;\n")

def reload_nginx():
    system("nginx -s reload")

while True:
    restart = False
    new_ips_backend = fetch_instance_ips("Backend")
    if backend != new_ips_backend:
        restart = True
        update_nginx_config("Backend", new_ips_backend)
        logging.info("Backends updated to => " + str(new_ips_backend))
        backend = new_ips_backend
    new_ips_frontend = fetch_instance_ips("Frontend")
    if frontend != new_ips_frontend:
        restart = True
        update_nginx_config("Frontend", new_ips_frontend)
        logging.info("Frontends updated to => " + str(new_ips_frontend))
        frontend = new_ips_frontend
    if restart:
        reload_nginx()
    sleep(1)