# 개요 
File path obj 가 아닌 객체로 인식 정확도가 매우 낮아졌다.    
인식 전에 기존 grok pattern 이 잘못 인식하는 file path 같은 obj를 제거해왔다.   
데이터 양이 커질 수록 예외 case 가 계속 발견되었다. (대부분 file path 같은 obj 때문에,,,)     

=> 기존 not_file_path pattern과 새로운 not_file_path pattern이 서로 다르게 인식하는 결과를 모아 분석

## 정리법
1. 로그
* 기존 not file pattern 인식 결과
* 새로운 not file pattern 인식 결과   
=> 문제점

## Cassandra_debug 로그 데이터
서로 다르게 인식하는 데이터 없음.

## Hadoop 로그 데이터
1. 2017-12-23 16:28:28,007 INFO org.apache.hadoop.yarn.server.resourcemanager.amlauncher.AMLauncher: Command to launch container container_1514014057225_0001_01_000001 : $JAVA_HOME/bin/java -Djava.io.tmpdir=$PWD/tmp -Dlog4j.configuration=container-log4j.properties -Dyarn.app.container.log.dir=<LOG_DIR> -Dyarn.app.container.log.filesize=0 -Dhadoop.root.logger=INFO,CLA -Dhadoop.root.logfile=syslog -Xmx1024m org.apache.hadoop.mapreduce.v2.app.MRAppMaster 1><LOG_DIR>/stdout 2><LOG_DIR>/stderr
- ['/stderr']
- ['/stdout', '/stderr']

## Mongo DB 로그 데이터
서로 다르게 인식하는 데이터 없음.

## OpenStack 로그 데이터
1. DEBUG keystone.server.flask.common [-] Adding resource routes to API ec2tokens: ['/ec2tokens' {}] {{(pid=1302) _add_mapped_resources /opt/stack/keystone/keystone/server/flask/common.py:422}}
- ['/opt/stack/keystone/keystone/server/flask/common.py:422']
- ['/ec2tokens', '/opt/stack/keystone/keystone/server/flask/common.py:422']

2. DEBUG keystone.server.flask.common [-] Adding resource routes to API OS-OAUTH1: ['/request_token' {}] {{(pid=1301) _add_mapped_resources /opt/stack/keystone/keystone/server/flask/common.py:422}}
- ['/opt/stack/keystone/keystone/server/flask/common.py:422']
- ['/request_token', '/opt/stack/keystone/keystone/server/flask/common.py:422']

3. DEBUG keystone.server.flask.common [-] Adding resource routes to API events: ['/events' {}] {{(pid=1302) _add_mapped_resources /opt/stack/keystone/keystone/server/flask/common.py:422}}
- ['/opt/stack/keystone/keystone/server/flask/common.py:422']
- ['/events', '/opt/stack/keystone/keystone/server/flask/common.py:422']

4. DEBUG keystone.server.flask.common [-] Adding resource routes to API role_assignments: ['/role_assignments' {}] {{(pid=1302) _add_mapped_resources /opt/stack/keystone/keystone/server/flask/common.py:422}}
- ['/opt/stack/keystone/keystone/server/flask/common.py:422']
- ['/role_assignments', '/opt/stack/keystone/keystone/server/flask/common.py:422']

5. DEBUG keystone.server.flask.common [-] Adding resource routes to API s3tokens: ['/s3tokens' {}] {{(pid=1302) _add_mapped_resources /opt/stack/keystone/keystone/server/flask/common.py:422}}
- ['/opt/stack/keystone/keystone/server/flask/common.py:422']
- ['/s3tokens', '/opt/stack/keystone/keystone/server/flask/common.py:422']

6. DEBUG nova.virt.libvirt.vif [None req-d1363ff9-98a6-4683-8d9d-df53c55a5917 None None] vif_type=ovs instance=Instance(access_ip_v4=None,access_ip_v6=None,architecture=None,auto_disk_config=True,availability_zone='nova',cell_name=None,cleaned=False,config_drive='',created_at=2019-07-31T08:46:11Z,default_ephemeral_device=None,default_swap_device=None,deleted=False,deleted_at=None,device_metadata=<?>,disable_terminate=False,display_description=None,display_name='리중딱',ec2_ids=<?>,ephemeral_gb=0,ephemeral_key_uuid=None,fault=<?>,flavor=<?>,host='triton11',hostname='Server-2d4c489e-83f6-40e4-b7cc-cfb12692bbf9',id=1,image_ref='bb240150-159c-4ea5-b04e-966fd0dbffbf',info_cache=InstanceInfoCache,instance_type_id=11,kernel_id='',key_data='ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDFFhOE6Qp1OPVgucRavRsx1riSiVIottcZSMAqjER2XD2/pLs043WwCeSoVHuv6GvOkztrOce0C98ItMrDbhl8Vn2gGQKvTL8+DiaoGXIxrN61xYSqFT748RhCX0OmtdkBU8MSKGD4+/flWYCyX02GHMpE3zatYeOU8K6RVVBmfKHvs+nl/xSw+Pc91rCKw+2/vNv2j56rWbE6Zr0Ig1YhEms7ci4o+SvaAFWUEjWlW82Yg0YFIDBp1yI0lDcrkXAt9MY6O035TpBrlzb//oUwNa2YlIhxv5HvrvlJQG+XZY/w7GZYgZ2z1oafIBd8FwPm+ZDA4ZK5m8rCAy477jB/ Generated-by-Nova',key_name='seorin',keypairs=<?>,launch_index=0,launched_at=2019-07-31T08:46:21Z,launched_on='triton11',locked=False,locked_by=None,memory_mb=64,metadata={},migration_context=<?>,new_flavor=<?>,node='triton11',numa_topology=<?>,old_flavor=<?>,os_type=None,pci_devices=<?>,pci_requests=<?>,power_state=1,progress=0,project_id='3efed2c1d335441296b8b2930d0a9b97',ramdisk_id='',reservation_id='r-smzekphf',root_device_name='/dev/vda',root_gb=1,security_groups=<?>,services=<?>,shutdown_terminate=False,system_metadata=<?>,tags=<?>,task_state=None,terminated_at=None,trusted_certs=<?>,updated_at=2019-07-31T08:46:22Z,user_data=None,user_id='3ef4e5dd63784f898967ce004a2760d0',uuid=2d4c489e-83f6-40e4-b7cc-cfb12692bbf9,vcpu_model=<?>,vcpus=1,vm_mode=None,vm_state='active') vif={"profile": {}, "ovs_interfaceid": "9a123c5c-bf15-4cbd-85d4-fba57fe62334", "preserve_on_delete": false, "network": {"bridge": "br-int",
- ['+/flWYCyX02GHMpE3zatYeOU8K6RVVBmfKHvs+nl/xSw+Pc91rCKw+2/vNv2j56rWbE6Zr0Ig1YhEms7ci4o+SvaAFWUEjWlW82Yg0YFIDBp1yI0lDcrkXAt9MY6O035TpBrlzb//oUwNa2YlIhxv5HvrvlJQG+XZY/w7GZYgZ2z1oafIBd8FwPm+ZDA4ZK5m8rCAy477jB/', "/dev/vda',root_gb=1,security_groups=<?>,services=<?>,shutdown_terminate=False,system_metadata=<?>,tags=<?>,task_state=None,terminated_at=None,trusted_certs=<?>,updated_at=2019-07-31T08:46:22Z,user_data=None,user_id='3ef4e5dd63784f898967ce004a2760d0',uuid=2d4c489e-83f6-40e4-b7cc-cfb12692bbf9,vcpu_model=<?>,vcpus=1,vm_mode=None,vm_state='active"]
- ['+/flWYCyX02GHMpE3zatYeOU8K6RVVBmfKHvs+nl/xSw+Pc91rCKw+2/vNv2j56rWbE6Zr0Ig1YhEms7ci4o+SvaAFWUEjWlW82Yg0YFIDBp1yI0lDcrkXAt9MY6O035TpBrlzb//oUwNa2YlIhxv5HvrvlJQG+XZY/w7GZYgZ2z1oafIBd8FwPm+ZDA4ZK5m8rCAy477jB/', "/dev/vda',root_gb=1,security_groups=<?>,services=<?>,shutdown_terminate=False,system_metadata=<?>,tags=<?>,task_state=None,terminated_at=None,trusted_certs=<?>,updated_at"]

7. DEBUG glance.api.middleware.version_negotiation [None req-6e2682d5-3d9f-4625-8c9c-e11bbc815796 demo admin] Determining version of request: GET /v2/images Accept: */* {{(pid=1308) process_request /opt/stack/glance/glance/api/middleware/version_negotiation.py:45}}
- ['/opt/stack/glance/glance/api/middleware/version_negotiation.py:45']
- ['*/*', '/opt/stack/glance/glance/api/middleware/version_negotiation.py:45']   
=> * / * : MIME Type (클라이언트에게 전송된 문서의 다양성을 알려주기 위한 메커니즘)   
=> MIME-Type 은 규칙이 정해져 있으니 Pattern 으로 만들어보는 방법도 좋을 거 같다!!!

8. DEBUG neutron.agent.resource_cache [None req-68dad1d4-24c4-4ec7-9a90-90b1df6ca980 None None] Received new resource SecurityGroupRule: SecurityGroupRule(created_at=2019-07-31T08:42:28Z,description='',direction='ingress',ethertype='IPv4',id=2049485e-dce2-4a7f-9eee-9591db38b491,port_range_max=22,port_range_min=22,project_id='3efed2c1d335441296b8b2930d0a9b97',protocol='tcp',remote_group_id=<?>,remote_ip_prefix=0.0.0.0/0,revision_number=0,security_group_id=07c471dd-e29f-402d-8f10-65cd0f99e3f3,updated_at=2019-07-31T08:42:28Z) {{(pid=1137) record_resource_update /opt/stack/neutron/neutron/agent/resource_cache.py:192}}
- ['/opt/stack/neutron/neutron/agent/resource_cache.py:192']
- ['/0,revision_number=0,security_group_id=07c471dd-e29f-402d-8f10-65cd0f99e3f3,updated_at', '/opt/stack/neutron/neutron/agent/resource_cache.py:192']

9. DEBUG neutron.agent.linux.openvswitch_firewall.firewall [None req-68dad1d4-24c4-4ec7-9a90-90b1df6ca980 None None] RULGEN: Rules generated for flow {'direction': u'ingress', 'protocol': 6, 'ethertype': u'IPv4', 'port_range_max': 22, 'source_ip_prefix': '0.0.0.0/0', 'port_range_min': 22} are [{'dl_type': 2048, 'reg_port': 17, 'nw_proto': 6, 'tcp_dst': '0x0016', 'table': 82, 'actions': 'output:17', 'priority': 77}] {{(pid=1137) add_flows_from_rules /opt/stack/neutron/neutron/agent/linux/openvswitch_firewall/firewall.py:1190}}
- ['/opt/stack/neutron/neutron/agent/linux/openvswitch_firewall/firewall.py:1190']
- ['/0', '/opt/stack/neutron/neutron/agent/linux/openvswitch_firewall/firewall.py:1190']

## Spark 로그 데이터
1. 19/02/17 17:17:47 DEBUG Client: {{JAVA_HOME}}/bin/java -server -Xmx512m -Djava.io.tmpdir={{PWD}}/tmp -Dspark.yarn.app.container.log.dir=<LOG_DIR> org.apache.spark.deploy.yarn.ExecutorLauncher --arg 'master:32987' --properties-file {{PWD}}/spark_conf/spark_conf.properties 1> <LOG_DIR>/stdout 2> <LOG_DIR>/stderr
- ['/bin/java', '/spark_conf/spark_conf.properties', '/stderr']
- ['/bin/java', '/tmp', '/spark_conf/spark_conf.properties', '/stdout', '/stderr']
