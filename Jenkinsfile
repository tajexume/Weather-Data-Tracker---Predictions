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
        powershell '.\\venv\\Scripts\\activate.ps1'
        powershell 'ls'
      }
    }

    stage('Collect Weather Data') {
      steps {
        sh '''bat venv/bin/activate.bat
python3 -m weather_cli --city \'Tokyo\'
python3 -m weather_cli --city \'Charlotte\'
python3 -m weather_cli --city \'San Jose\'
python3 -m weather_cli --city \'Los Angeles\'
python3 -m weather_cli --city \'New York\''''
      }
    }

  }
}