server {
    listen 80;
    server_name  ec2-50-112-40-8.us-west-2.compute.amazonaws.com;
    access_log /var/log/nginx/access.log;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real_IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}