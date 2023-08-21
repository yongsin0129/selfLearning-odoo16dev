# run odoo server
docker-compose up

cd odoo-16.0/
python3 odoo-bin -c config/odoo.conf

# check db
psql -h localhost -U odoo -d postgres

# check all port state
sudo ps
sudo ss -tuln

-t: 顯示 TCP 協議的連接
-u: 顯示 UDP 協議的連接
-l: 只顯示正在監聽的連接
-n: 以數字形式顯示埠號，而不是埠號對應的服務名稱

```
sudo ps 和 sudo ss 是兩個不同的命令，用於查詢系統中運行的進程和網絡連接的信息。

sudo ps：ps 命令用於查詢系統中運行的進程。通過執行 sudo ps 命令，你可以獲取有關進程的詳細信息，如進程 ID（PID）、執行狀態、CPU 和內存使用情況等。這個命令主要用於查看系統中正在運行的進程以及它們的屬性。

sudo ss：ss 命令用於查詢系統的網絡連接信息。它可以顯示當前的 TCP 和 UDP 連接，包括本地地址、本地埠號、遠程地址、遠程埠號以及連接狀態等。這個命令主要用於查看系統中的網絡連接和相關的屬性。

總結來說，sudo ps 用於查詢進程信息，而 sudo ss 用於查詢網絡連接信息。它們提供不同層面的系統信息，並可用於不同的目的。
```

# search id from specific ps and kill
sudo lsof -t -i:8069
sudo kill <PID>