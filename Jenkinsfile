pipeline {
  agent any
  stages {
    stage('Iniciando enviroment') {
      steps {
        echo 'Inicializando...'
        sh 'env'
      }
    }

    stage('docker Env') {
      steps {
        sh 'docker --version'
      }
    }

    stage('Build') {
      steps {
        sh 'docker'
      }
    }

  }
}