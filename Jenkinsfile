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
        sh 'cat versionImage | xargs ./scripts/build.sh'
      }
    }

    stage('Correr contenedor') {
      steps {
        sh '''docker stop proyapi || true
docker run --name proyapi -itd --rm -p 5000:5000 malagoiram/proyectoapi:1.1 '''
      }
    }

    stage('Test - QA') {
      steps {
        sleep 10
        sh './scripts/test_container.sh'
      }
    }

    stage('publicar') {
      steps {
        sh 'docker push malagoiram/proyectoapi:1.1 '
      }
    }

  }
}