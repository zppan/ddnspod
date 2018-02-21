# ddnspod
自动更新本机IP到 dnspod.cn

修改democonfig.json内容 { "id":"71688",           # dnspod.cn上注册的ID number "token":"716882sdews",  # dnspod.cn上申请的 token "domain":"demo.com",    # 域名 "sub_domain":"sub"      # 需要指向当前主机的子域名(sub.demo.com) } 
运行 python -m ddnspod ./democonfig.json
