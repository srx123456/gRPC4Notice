class ExploreFormat:
    def __init__(self, instance_id, control_param, service_type, instance_state, instance_version,
                 destination_address, current_hop, max_hop, ttl, heartbeat, return_port, return_address, extension):
        self.instance_id = instance_id                    # 实例标识 (2 bytes)
        self.control_param = control_param                # 控制参数 (2 bytes)
        self.service_type = service_type                  # 服务类型 (2 bytes)
        self.instance_state = instance_state              # 实例状态 (1 byte)
        self.instance_version = instance_version          # 实例版本 (1 byte)
        self.destination_address = destination_address    # 服务的目的地址 (4 bytes)
        self.current_hop = current_hop                    # 当前跳数 (1 byte)
        self.max_hop = max_hop                            # 最大跳数 (1 byte)
        self.ttl = ttl                                    # 报文生存时间 (2 bytes)
        self.heartbeat = heartbeat                        # 心跳消息 (2 bytes)
        self.return_port = return_port                    # 返回端口 (2 bytes)
        self.return_address = return_address              # 返回地址 (4 bytes)
        self.extension = extension                        # 扩展 (4 bytes)

    def __repr__(self):
        return (f"ExploreFormat(instance_id={self.instance_id}, control_param={self.control_param}, "
                f"service_type={self.service_type}, instance_state={self.instance_state}, "
                f"instance_version={self.instance_version}, destination_address={self.destination_address}, "
                f"current_hop={self.current_hop}, max_hop={self.max_hop}, ttl={self.ttl}, "
                f"heartbeat={self.heartbeat}, return_port={self.return_port}, "
                f"return_address={self.return_address}, extension={self.extension})")
    
