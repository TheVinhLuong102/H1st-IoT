resource "aws_elasticache_cluster" "pm-cache" {
  cluster_id           = "pm-aidb-cache"
  engine               = "redis"
  node_type            = "cache.m3.medium"
  num_cache_nodes      = 1
  parameter_group_name = "default.redis5.0"
  engine_version       = "5.0.4"
  port                 = 6379
}

