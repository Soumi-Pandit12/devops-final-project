pipeline {
    agent any
    environment {
        // REPLACE 'your_dockerhub_username' with your actual Docker Hub username
        DOCKER_USER = "your_dockerhub_username" 
        IMAGE_NAME  = "quicknotes-final"
    }
    stages {
        stage('Build Image') {
            steps {
                sh "docker build -t $DOCKER_USER/$IMAGE_NAME:latest ."
            }
        }
        stage('Push to Docker Hub') {
            steps {
                // This assumes you have run 'docker login' on the EC2 server manually once
                sh "docker push $DOCKER_USER/$IMAGE_NAME:latest"
            }
        }
        stage('Deploy with Compose') {
            steps {
                // Using Docker Compose to restart the service with the new image
                sh "docker-compose down || true"
                sh "DOCKER_USER=$DOCKER_USER docker-compose up -d"
            }
        }
    }
}