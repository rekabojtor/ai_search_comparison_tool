data "aws_vpc" "default" {
  default = true
}
data "http" "my_ip" {
  url = "https://checkip.amazonaws.com/"
}

data "local_file" "ssh_key" {
  filename = "/Users/rekabojtor/.ssh/id_ed25519.pub"
}

resource "aws_key_pair" "default" {
  key_name   = "reka-terraform"
  public_key = data.local_file.ssh_key.content
}

resource "aws_security_group" "default" {
  name        = "allow_ssh_reka"
  description = "Allow SSH inbound traffic from my IP"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description      = "SSH from my IP"
    from_port        = 22
    to_port          = 22
    protocol         = "tcp"
    cidr_blocks      = ["${chomp(data.http.my_ip.response_body)}/32"]
  }
}

resource "aws_instance" "default" {
  ami           = "ami-015f3aa67b494b27e"
  instance_type = "t2.micro"
  key_name      = aws_key_pair.default.key_name
  vpc_security_group_ids = [aws_security_group.default.id]

  root_block_device {
    volume_size           = 8
    volume_type           = "gp3"
    delete_on_termination = true
  }

  tags = {
    Name = "reka-terraform"
  }
}

output "instance_public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = aws_instance.default.public_ip
}

output "ssh_command" {
  description = "SSH command to connect to the instance"
  value       = "ssh ec2-user@${aws_instance.default.public_ip}"
}