output "rds_endpoint" {
  value       = aws_db_instance.db.endpoint
  description = "The endpoint of the RDS instance"
  depends_on  = [aws_db_instance.db]
}
