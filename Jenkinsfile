pipeline {
    agent any

    environment {
        IMAGE_NAME = 'flask-app'
        CONTAINER_NAME = 'quicknotes-app'
        RDS_HOST = 'terraform-20260428030748881300000001.cnqimo8iklww.ap-south-1.rds.amazonaws.com'
        DB_USER = 'admin'
        DB_PASS = 'password123'
        DB_NAME = 'mydb'
    }

    stages {

        stage('Clone Code') {
            steps {
                git url: 'https://github.com/Soumi-Pandit12/quicknotes-flask-mysql-docker.git', branch: 'main'
            }
        }

        stage('Build Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Stop Old Container') {
            steps {
                sh 'docker stop $CONTAINER_NAME || true'
                sh 'docker rm $CONTAINER_NAME || true'
            }
        }

        stage('Run Container') {
            steps {
                sh '''
                docker run -d \
                  --name $CONTAINER_NAME \
                  -p 5000:5000 \
                  -e MYSQL_HOST=$RDS_HOST \
                  -e MYSQL_USER=$DB_USER \
                  -e MYSQL_PASSWORD=$DB_PASS \
                  -e MYSQL_DB=$DB_NAME \
                  $IMAGE_NAME
                '''
            }
        }
    }
}
