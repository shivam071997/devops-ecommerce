pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out E-Commerce DevOps project'
                checkout scm
            }
        }

        stage('Verify Tools') {
            steps {
                sh 'git --version'
                sh 'docker --version'
                sh 'docker compose version'
            }
        }

        stage('Build Backend') {
            steps {
                sh 'docker build -t ecommerce-backend:jenkins ./backend'
            }
        }

        stage('Build Frontend') {
            steps {
                sh 'docker build -t ecommerce-frontend:jenkins ./frontend'
            }
        }

        stage('Verify Images') {
            steps {
                sh 'docker images | grep ecommerce-'
            }
        }
    }
}
