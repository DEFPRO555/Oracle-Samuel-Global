# © 2025 Dowek Analytics Ltd.
# Oracle Samuel - AWS Infrastructure (Terraform)

terraform {
  required_version = ">= 1.5.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  backend "s3" {
    bucket = "oracle-samuel-terraform-state"
    key    = "terraform/state"
    region = "us-east-1"
  }
}

provider "aws" {
  region = var.region
}

# Variables
variable "region" {
  description = "AWS Region"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment (dev/staging/prod)"
  type        = string
  default     = "production"
}

variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}

# VPC
resource "aws_vpc" "oracle_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = {
    Name        = "oracle-samuel-vpc-${var.environment}"
    Environment = var.environment
  }
}

# Subnets
resource "aws_subnet" "public_1" {
  vpc_id            = aws_vpc.oracle_vpc.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "${var.region}a"
  
  map_public_ip_on_launch = true
  
  tags = {
    Name = "oracle-public-subnet-1"
  }
}

resource "aws_subnet" "public_2" {
  vpc_id            = aws_vpc.oracle_vpc.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "${var.region}b"
  
  map_public_ip_on_launch = true
  
  tags = {
    Name = "oracle-public-subnet-2"
  }
}

resource "aws_subnet" "private_1" {
  vpc_id            = aws_vpc.oracle_vpc.id
  cidr_block        = "10.0.10.0/24"
  availability_zone = "${var.region}a"
  
  tags = {
    Name = "oracle-private-subnet-1"
  }
}

resource "aws_subnet" "private_2" {
  vpc_id            = aws_vpc.oracle_vpc.id
  cidr_block        = "10.0.11.0/24"
  availability_zone = "${var.region}b"
  
  tags = {
    Name = "oracle-private-subnet-2"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "oracle_igw" {
  vpc_id = aws_vpc.oracle_vpc.id
  
  tags = {
    Name = "oracle-igw"
  }
}

# NAT Gateway
resource "aws_eip" "nat" {
  domain = "vpc"
}

resource "aws_nat_gateway" "oracle_nat" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public_1.id
  
  tags = {
    Name = "oracle-nat-gateway"
  }
}

# Route Tables
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.oracle_vpc.id
  
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.oracle_igw.id
  }
  
  tags = {
    Name = "oracle-public-rt"
  }
}

resource "aws_route_table" "private" {
  vpc_id = aws_vpc.oracle_vpc.id
  
  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.oracle_nat.id
  }
  
  tags = {
    Name = "oracle-private-rt"
  }
}

resource "aws_route_table_association" "public_1" {
  subnet_id      = aws_subnet.public_1.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "public_2" {
  subnet_id      = aws_subnet.public_2.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "private_1" {
  subnet_id      = aws_subnet.private_1.id
  route_table_id = aws_route_table.private.id
}

resource "aws_route_table_association" "private_2" {
  subnet_id      = aws_subnet.private_2.id
  route_table_id = aws_route_table.private.id
}

# Security Groups
resource "aws_security_group" "alb_sg" {
  name        = "oracle-alb-sg"
  description = "Security group for ALB"
  vpc_id      = aws_vpc.oracle_vpc.id
  
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "ecs_sg" {
  name        = "oracle-ecs-sg"
  description = "Security group for ECS tasks"
  vpc_id      = aws_vpc.oracle_vpc.id
  
  ingress {
    from_port       = 0
    to_port         = 65535
    protocol        = "tcp"
    security_groups = [aws_security_group.alb_sg.id]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "rds_sg" {
  name        = "oracle-rds-sg"
  description = "Security group for RDS"
  vpc_id      = aws_vpc.oracle_vpc.id
  
  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.ecs_sg.id]
  }
}

resource "aws_security_group" "redis_sg" {
  name        = "oracle-redis-sg"
  description = "Security group for ElastiCache Redis"
  vpc_id      = aws_vpc.oracle_vpc.id
  
  ingress {
    from_port       = 6379
    to_port         = 6379
    protocol        = "tcp"
    security_groups = [aws_security_group.ecs_sg.id]
  }
}

# RDS PostgreSQL
resource "aws_db_subnet_group" "oracle_db_subnet" {
  name       = "oracle-db-subnet-group"
  subnet_ids = [aws_subnet.private_1.id, aws_subnet.private_2.id]
  
  tags = {
    Name = "Oracle DB Subnet Group"
  }
}

resource "aws_db_instance" "oracle_postgres" {
  identifier     = "oracle-samuel-postgres-${var.environment}"
  engine         = "postgres"
  engine_version = "15.5"
  instance_class = "db.t3.large"
  
  allocated_storage     = 100
  max_allocated_storage = 500
  storage_type          = "gp3"
  storage_encrypted     = true
  
  db_name  = "oracle_db"
  username = "oracle"
  password = var.db_password
  
  multi_az               = true
  db_subnet_group_name   = aws_db_subnet_group.oracle_db_subnet.name
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  
  backup_retention_period = 30
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"
  
  enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]
  
  skip_final_snapshot = false
  final_snapshot_identifier = "oracle-postgres-final-${var.environment}"
  
  tags = {
    Name        = "Oracle PostgreSQL"
    Environment = var.environment
  }
}

# ElastiCache Redis
resource "aws_elasticache_subnet_group" "oracle_redis_subnet" {
  name       = "oracle-redis-subnet-group"
  subnet_ids = [aws_subnet.private_1.id, aws_subnet.private_2.id]
}

resource "aws_elasticache_replication_group" "oracle_redis" {
  replication_group_id       = "oracle-redis-${var.environment}"
  description                = "Oracle Samuel Redis Cluster"
  engine                     = "redis"
  engine_version             = "7.0"
  node_type                  = "cache.t3.medium"
  num_cache_clusters         = 2
  parameter_group_name       = "default.redis7"
  port                       = 6379
  subnet_group_name          = aws_elasticache_subnet_group.oracle_redis_subnet.name
  security_group_ids         = [aws_security_group.redis_sg.id]
  automatic_failover_enabled = true
  at_rest_encryption_enabled = true
  transit_encryption_enabled = false
  
  snapshot_retention_limit = 5
  snapshot_window         = "03:00-05:00"
  
  tags = {
    Name        = "Oracle Redis"
    Environment = var.environment
  }
}

# S3 Buckets
resource "aws_s3_bucket" "models" {
  bucket = "oracle-samuel-models-${var.environment}-${data.aws_caller_identity.current.account_id}"
  
  tags = {
    Name        = "Oracle Models"
    Environment = var.environment
  }
}

resource "aws_s3_bucket_versioning" "models_versioning" {
  bucket = aws_s3_bucket.models.id
  
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "models_lifecycle" {
  bucket = aws_s3_bucket.models.id
  
  rule {
    id     = "archive-old-models"
    status = "Enabled"
    
    transition {
      days          = 90
      storage_class = "STANDARD_IA"
    }
    
    transition {
      days          = 365
      storage_class = "GLACIER"
    }
  }
}

resource "aws_s3_bucket" "uploads" {
  bucket = "oracle-samuel-uploads-${var.environment}-${data.aws_caller_identity.current.account_id}"
  
  tags = {
    Name        = "Oracle Uploads"
    Environment = var.environment
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "uploads_lifecycle" {
  bucket = aws_s3_bucket.uploads.id
  
  rule {
    id     = "delete-old-uploads"
    status = "Enabled"
    
    expiration {
      days = 30
    }
  }
}

# ECR Repositories
resource "aws_ecr_repository" "backend" {
  name                 = "oracle-backend"
  image_tag_mutability = "MUTABLE"
  
  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_repository" "frontend" {
  name                 = "oracle-frontend"
  image_tag_mutability = "MUTABLE"
  
  image_scanning_configuration {
    scan_on_push = true
  }
}

# ECS Cluster
resource "aws_ecs_cluster" "oracle_cluster" {
  name = "oracle-samuel-cluster-${var.environment}"
  
  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

# ECS Task Execution Role
resource "aws_iam_role" "ecs_task_execution_role" {
  name = "oracle-ecs-task-execution-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ecs-tasks.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_role_policy" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# ECS Task Role
resource "aws_iam_role" "ecs_task_role" {
  name = "oracle-ecs-task-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ecs-tasks.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy" "ecs_task_s3_policy" {
  name = "oracle-ecs-s3-policy"
  role = aws_iam_role.ecs_task_role.id
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:ListBucket"
      ]
      Resource = [
        aws_s3_bucket.models.arn,
        "${aws_s3_bucket.models.arn}/*",
        aws_s3_bucket.uploads.arn,
        "${aws_s3_bucket.uploads.arn}/*"
      ]
    }]
  })
}

# CloudWatch Log Groups
resource "aws_cloudwatch_log_group" "backend" {
  name              = "/ecs/oracle-backend"
  retention_in_days = 30
}

resource "aws_cloudwatch_log_group" "frontend" {
  name              = "/ecs/oracle-frontend"
  retention_in_days = 30
}

# ECS Task Definition - Backend
resource "aws_ecs_task_definition" "backend" {
  family                   = "oracle-backend"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "1024"
  memory                   = "2048"
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn           = aws_iam_role.ecs_task_role.arn
  
  container_definitions = jsonencode([{
    name  = "backend"
    image = "${aws_ecr_repository.backend.repository_url}:latest"
    
    portMappings = [{
      containerPort = 8000
      protocol      = "tcp"
    }]
    
    environment = [
      {
        name  = "DATABASE_URL"
        value = "postgresql://oracle:${var.db_password}@${aws_db_instance.oracle_postgres.endpoint}/oracle_db"
      },
      {
        name  = "REDIS_URL"
        value = "redis://${aws_elasticache_replication_group.oracle_redis.primary_endpoint_address}:6379"
      },
      {
        name  = "S3_BUCKET"
        value = aws_s3_bucket.models.bucket
      },
      {
        name  = "AWS_REGION"
        value = var.region
      }
    ]
    
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        "awslogs-group"         = aws_cloudwatch_log_group.backend.name
        "awslogs-region"        = var.region
        "awslogs-stream-prefix" = "ecs"
      }
    }
    
    healthCheck = {
      command     = ["CMD-SHELL", "curl -f http://localhost:8000/health || exit 1"]
      interval    = 30
      timeout     = 5
      retries     = 3
      startPeriod = 60
    }
  }])
}

# ECS Service - Backend
resource "aws_ecs_service" "backend" {
  name            = "oracle-backend-service"
  cluster         = aws_ecs_cluster.oracle_cluster.id
  task_definition = aws_ecs_task_definition.backend.arn
  desired_count   = 2
  launch_type     = "FARGATE"
  
  network_configuration {
    subnets         = [aws_subnet.private_1.id, aws_subnet.private_2.id]
    security_groups = [aws_security_group.ecs_sg.id]
  }
  
  load_balancer {
    target_group_arn = aws_lb_target_group.backend.arn
    container_name   = "backend"
    container_port   = 8000
  }
  
  depends_on = [aws_lb_listener.https]
}

# Application Load Balancer
resource "aws_lb" "oracle_alb" {
  name               = "oracle-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb_sg.id]
  subnets           = [aws_subnet.public_1.id, aws_subnet.public_2.id]
  
  enable_deletion_protection = true
  
  tags = {
    Name        = "Oracle ALB"
    Environment = var.environment
  }
}

# Target Groups
resource "aws_lb_target_group" "backend" {
  name        = "oracle-backend-tg"
  port        = 8000
  protocol    = "HTTP"
  vpc_id      = aws_vpc.oracle_vpc.id
  target_type = "ip"
  
  health_check {
    path                = "/health"
    healthy_threshold   = 2
    unhealthy_threshold = 3
    timeout             = 5
    interval            = 30
    matcher             = "200"
  }
}

resource "aws_lb_target_group" "frontend" {
  name        = "oracle-frontend-tg"
  port        = 8501
  protocol    = "HTTP"
  vpc_id      = aws_vpc.oracle_vpc.id
  target_type = "ip"
  
  health_check {
    path                = "/_stcore/health"
    healthy_threshold   = 2
    unhealthy_threshold = 3
    timeout             = 5
    interval            = 30
    matcher             = "200"
  }
}

# ALB Listeners
resource "aws_lb_listener" "https" {
  load_balancer_arn = aws_lb.oracle_alb.arn
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS-1-2-2017-01"
  certificate_arn   = var.certificate_arn
  
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.frontend.arn
  }
}

# Data sources
data "aws_caller_identity" "current" {}

# Outputs
output "alb_dns_name" {
  value       = aws_lb.oracle_alb.dns_name
  description = "ALB DNS name"
}

output "rds_endpoint" {
  value       = aws_db_instance.oracle_postgres.endpoint
  description = "RDS endpoint"
  sensitive   = true
}

output "redis_endpoint" {
  value       = aws_elasticache_replication_group.oracle_redis.primary_endpoint_address
  description = "Redis endpoint"
}

output "models_bucket" {
  value       = aws_s3_bucket.models.bucket
  description = "Models S3 bucket"
}

output "backend_ecr" {
  value       = aws_ecr_repository.backend.repository_url
  description = "Backend ECR repository URL"
}

output "frontend_ecr" {
  value       = aws_ecr_repository.frontend.repository_url
  description = "Frontend ECR repository URL"
}

