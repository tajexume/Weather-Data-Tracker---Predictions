pipeline {
  agent any
  stages {
    stage('Clone Repo') {
      steps {
        git(url: 'https://github.com/tajexume/Weather-Data-Tracker---Predictions.git', branch: 'main')
      }
    }

    stage('Create VENV') {
      steps {
        powershell '.\\.venv\\Scripts\\Activate.ps1'
      }
    }

    stage('Collect Weather Data') {
      steps {
        powershell(script: 'python3 -m weather_cli --city \'San Jose\'', returnStdout: true)
      }
    }

  }
  environment {
    python3 = '":\\Python312\\python.exe'
  }
}