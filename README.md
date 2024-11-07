Say interesting things


python3 -m venv venv
source venv/bin/activate
pip3 install Flask pandas toml openpyxl xlrd gunicorn


/etc/systemd/system/

sudo systemctl daemon-reload
sudo systemctl start xls_combiner
sudo systemctl enable xls_combiner

sudo systemctl status xls_combiner