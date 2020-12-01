pipeline {
  agent any
  stages {
    stage('Iniciando enviroment') {
      steps {
        echo 'Inicializando...'
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