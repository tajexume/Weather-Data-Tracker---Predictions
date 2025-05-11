pipeline {
  agent any
  stages {
    stage('Clone Repo') {
      steps {
        git(url: 'https://github.com/tajexume/Weather-Data-Tracker---Predictions.git', branch: 'main')
      }
    }

    stage('runs script') {
      steps {
        powershell '.\\.venv\\Scripts\\Activate.ps1'
        powershell(script: '.\\utils\\run_script.ps1', returnStdout: true)
      }
    }

  }
  environment {
    python3 = '":\\Python312\\python.exe'
  }
}