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
<<<<<<< HEAD
    python3 = '"C:\\Python312\\python.exe'
=======
    python3 = 'C:\\Python312\\python.exe'
>>>>>>> 11580eba10e2bcd8e12f0a8dde9c35c5ee2dc475
  }
}