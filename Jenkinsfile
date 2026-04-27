pipeline {
    agent any
    environment {
        // REPLACE with your actual Docker Hub ID
        DOCKER_USER = "your_dockerhub_username" 
        IMAGE_NAME  = "quicknotes-final"
        // YOUR LATEST AWS IP
        TARGET_IP   = "13.126.250.134"             
        // The ID of your SSH Key stored in Jenkins Credentials
        SSH_KEY_ID  = "final-server-key"        
    }
    stages {
        stage('Build Image') {
            steps {
                sh "docker build -t $DOCKER_USER/$IMAGE_NAME:latest ."
            }
        }
        stage('Push to Docker Hub') {
            steps {
                // This assumes your Jenkins Master is logged into Docker Hub
                sh "docker push $DOCKER_USER/$IMAGE_NAME:latest"
            }
        }
        stage('Deploy to New EC2') {
            steps {
                sshagent([SSH_KEY_ID]) {
                    sh """
                    ssh -o StrictHostKeyChecking=no ubuntu@$TARGET_IP '
                        # Clean up old containers if they exist
                        docker stop my-running-app || true
                        docker rm my-running-app || true
                        docker pull $DOCKER_USER/$IMAGE_NAME:latest
                        # Run the new container on Port 80
                        docker run -d --name my-running-app -p 80:5000 $DOCKER_USER/$IMAGE_NAME:latest
                    '
                    """
                }
            }
        }
    }
}