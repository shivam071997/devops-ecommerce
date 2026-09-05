pipeline {
    agent any

    environment {
        DOCKERHUB_USER = 'shivam0708'
        BACKEND_IMAGE = 'shivam0708/ecommerce-backend'
        FRONTEND_IMAGE = 'shivam0708/ecommerce-frontend'
    }

    stages {

        stage('Checkout') {
            steps {
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
                sh 'docker build -t ${BACKEND_IMAGE}:${BUILD_NUMBER} ./backend'
            }
        }

        stage('Build Frontend') {
            steps {
                sh 'docker build -t ${FRONTEND_IMAGE}:${BUILD_NUMBER} ./frontend'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_TOKEN'
                )]) {
                    sh '''
                        echo "$DOCKER_TOKEN" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push ${BACKEND_IMAGE}:${BUILD_NUMBER}
                        docker push ${FRONTEND_IMAGE}:${BUILD_NUMBER}
                        docker logout
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    kubectl --kubeconfig=/var/lib/jenkins/.kube/config set image deployment/ecommerce-backend                       ecommerce-backend=${BACKEND_IMAGE}:${BUILD_NUMBER}

                    kubectl --kubeconfig=/var/lib/jenkins/.kube/config set image deployment/ecommerce-frontend                       ecommerce-frontend=${FRONTEND_IMAGE}:${BUILD_NUMBER}

                    kubectl --kubeconfig=/var/lib/jenkins/.kube/config rollout status deployment/ecommerce-backend
                    kubectl --kubeconfig=/var/lib/jenkins/.kube/config rollout status deployment/ecommerce-frontend
                '''
            }
        }
    }
}
