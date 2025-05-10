pipeline {
  agent any
  stages {
    stage('Clone Repo') {
      steps {
        git(url: 'https://github.com/tajexume/Weather-Data-Tracker---Predictions.git', branch: 'main')
      }
    }

    stage('Create VENV') {
      parallel {
        stage('Create VENV') {
          steps {
            powershell '.\\.venv\\Scripts\\Activate.ps1'
          }
        }

        stage('') {
          steps {
            powershell 'C:\\Python312\\python.exe'
          }
        }

      }
    }

  }
  environment {
    python3 = '":\\Python312\\python.exe'
  }
}